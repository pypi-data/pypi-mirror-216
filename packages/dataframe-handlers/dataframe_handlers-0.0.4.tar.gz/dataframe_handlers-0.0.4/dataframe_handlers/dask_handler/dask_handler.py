from typing import Optional, Union

import dask.dataframe as dd

from ..pandas_handler import PandasDataFrameHandler


class DaskDataFrameHandler(PandasDataFrameHandler):
    df: dd.DataFrame

    def get_unique(self, column: str, limit: Optional[int] = None) -> dd.Series:
        unique_values_series = self.df[column].compute().unique()
        return (
            unique_values_series if limit is None else unique_values_series.head(limit)
        )

    def get_value_counts(
        self,
        column: str,
        limit: Optional[int] = None,
    ) -> dd.DataFrame:
        value_counts_df = (
            self.df[column].compute().value_counts(dropna=False).reset_index()
        )
        value_counts_df.columns = ["value", "count"]
        return value_counts_df if limit is None else value_counts_df.head(limit)

    def get_data_range(self, column: str) -> tuple:
        # self.df[column].divisions
        min_value = self.df[column].min().compute()
        max_value = self.df[column].max().compute()
        return (min_value, max_value)

    def get_column_types(
        self,
        default_str: bool = True,
    ) -> dict[str, Union[object, type, str]]:
        dtype_dict = {
            "i": int,
            "u": int,
            "f": float,
            "b": bool,
        }
        column_types = self.df.dtypes
        return column_types.apply(
            lambda dtype: dtype_dict.get(dtype.kind, str if default_str else dtype),
        ).to_dict()
