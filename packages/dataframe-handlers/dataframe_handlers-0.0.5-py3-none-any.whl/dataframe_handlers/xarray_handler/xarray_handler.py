import numpy as np
import pandas as pd
import xarray as xr

from typing import Optional, Union
from ..pandas_handler import PandasDataFrameHandler


class XarrayDataFrameHandler(PandasDataFrameHandler):
    df: xr.Dataset

    def get_unique(self, column: str, limit: Optional[int] = None) -> np.ndarray:
        unique_values_array = self.df[column].values.flatten()
        unique_values = np.unique(unique_values_array)
        return unique_values if limit is None else unique_values[:limit]

    def get_value_counts(
        self,
        column: str,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        value_counts_array = self.df[column].values.flatten()
        unique_values, counts = np.unique(value_counts_array, return_counts=True)
        value_counts_df = pd.DataFrame({"value": unique_values, "count": counts})
        value_counts_df = value_counts_df.sort_values("value").reset_index(drop=True)
        return value_counts_df if limit is None else value_counts_df.head(limit)

    def get_data_range(self, column: str) -> tuple:
        data_column = self.df[column]
        data_min = float(data_column.min().item())
        data_max = float(data_column.max().item())
        return (data_min, data_max)

    def get_missing_filter(self, column: str) -> xr.DataArray:
        return self.df[column].isnull()

    def get_value_filter(
        self,
        column: str,
        values: list,
        invert: bool = False,
    ) -> xr.DataArray:
        value_filter = xr.DataArray(
            np.isin(self.df[column].values, values),
            dims=self.df.dims,
        )
        return ~value_filter if invert else value_filter

    def get_columns(self) -> list[str]:
        return sorted(list(self.df.data_vars))

    def get_numeric_columns(self) -> list[str]:
        numeric_columns = [
            column
            for column, dtype in self.df.dtypes.items()
            if np.issubdtype(dtype, np.number)
        ]
        return numeric_columns

    def get_column_types(
        self,
        default_str: bool = True,
    ) -> dict[str, Union[object, type, str]]:
        dtype_dict = {
            "i": int,
            "u": int,
            "f": float,
            "b": bool,
            "M": "datetime64[ns]",
        }
        column_types = self.df.dtypes
        return {
            column: dtype_dict.get(dtype.kind, str if default_str else dtype)
            for column, dtype in column_types.items()
        }
