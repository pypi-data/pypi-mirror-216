# import vaex
# from typing import Optional
# from ..base import BaseDataFrameHandler
#
#
# class VaexDataFrameHandler(BaseDataFrameHandler):
#     df: vaex.dataframe.DataFrame
#
#     def __init__(self, df: vaex.dataframe.DataFrame):
#         super().__init__(df)
#
#     def get_unique(self, column: str, limit: Optional[int] = None) -> list:
#         return self.df.unique(
#             column,
#             limit=limit + 1 if limit else None,
#             limit_raise=False,
#         )
#
#     def get_value_counts(
#         self,
#         column: str,
#         limit: Optional[int] = None,
#     ) -> vaex.dataframe.DataFrame:
#         value_counts_df = (
#             self.df.groupby(
#                 column,
#                 agg="count",
#                 sort="count",
#                 ascending=False,
#             )
#             .to_pandas_df()
#             .rename(columns={column: "value"})
#         )
#         return value_counts_df if limit is None else value_counts_df.head(limit)
#
#     def get_data_range(self, column: str) -> tuple:
#         minmax = self.df[column].minmax()
#         return minmax[0].item(), minmax[1].item()
#
#     def get_missing_filter(self, column: str) -> vaex.expression.Expression:
#         return self.df[column].isna()
#
#     def get_value_filter(
#         self,
#         column: str,
#         values: list,
#         invert: bool = False,
#     ) -> vaex.expression.Expression:
#         _filter = self.df[column].isin(values)
#         return ~_filter if invert else _filter
#
#     def get_columns(self) -> list[str]:
#         return self.df.get_column_names()
#
#     def get_numeric_columns(self) -> list[str]:
#         return self.df.select(".*", exclude=["object"]).get_column_names()
#
#     def get_column_types(self, default_str: bool = True) -> dict:
#         schema = self.df.schema()
#         py_types = [int, float, str, bool]
#
#         def py_type(dtype):
#             for k in py_types:
#                 if dtype == k:
#                     return k
#             return dtype
#
#         return {name: py_type(dtype) for name, dtype in schema.items()}
