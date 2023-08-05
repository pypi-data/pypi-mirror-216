import dask.dataframe as dd
import pytest

from . import DataFrameHandlerTestBase, test_pandas_df


class TestDaskDataFrameHandler(DataFrameHandlerTestBase):
    @pytest.fixture
    def data(self):
        return dd.from_pandas(test_pandas_df, npartitions=2)
