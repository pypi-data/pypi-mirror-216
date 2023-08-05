import pytest
import xarray as xr

from . import DataFrameHandlerTestBase, test_pandas_df


class TestXarrayDataFrameHandler(DataFrameHandlerTestBase):
    @pytest.fixture
    def data(self):
        return xr.Dataset.from_dataframe(test_pandas_df)
