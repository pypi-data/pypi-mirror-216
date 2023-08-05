import pytest

from . import DataFrameHandlerTestBase, test_pandas_df


class TestPandasDataFrameHandler(DataFrameHandlerTestBase):
    @pytest.fixture
    def data(self):
        return test_pandas_df
