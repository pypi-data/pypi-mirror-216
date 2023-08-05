from typing import Any, Optional, Type

from .base import BaseDataFrameHandler

__version__ = "0.0.4"
__all__ = ["BaseDataFrameHandler"]

dispatch_dict = {}

try:
    import pandas as pd
    from .pandas_handler import PandasDataFrameHandler

    __all__.append("PandasDataFrameHandler")
    dispatch_dict[pd.DataFrame] = PandasDataFrameHandler

except ImportError:
    pass

try:
    import dask.dataframe as dd
    from .dask_handler import DaskDataFrameHandler

    __all__.append("DaskDataFrameHandler")
    dispatch_dict[dd.DataFrame] = DaskDataFrameHandler
except ImportError:
    pass

try:
    import xarray as xr
    from .xarray_handler import XarrayDataFrameHandler

    __all__.append("XarrayDataFrameHandler")
    dispatch_dict[xr.Dataset] = XarrayDataFrameHandler
except ImportError:
    pass

# try:
#     import vaex
#     from .vaex_handler import VaexDataFrameHandler
#
#     __all__.append("VaexDataFrameHandler")
#     dispatch_dict[vaex.dataframe.DataFrame] = VaexDataFrameHandler
# except ImportError:
#     pass


def get_handler(df: Any, handler_type: Optional[Type] = None) -> BaseDataFrameHandler:
    """
    Function to get the appropriate handler based on the dataframe type.

    Args:
        df (Any): The dataframe for which we want to get a handler.
        handler_type (Optional[Type]): An optional handler type. If provided, this function
        will instantiate a handler of this type with the dataframe `df` and return it.

    Returns:
        Returns the appropriate handler for the dataframe `df`. If `handler_type` is
        provided, it returns an instance of `handler_type`.

    Raises:
        NotImplementedError: If the dataframe's type does not have an associated handler in
        `dispatch_dict`, and `handler_type` is not provided or None, it raises a
        NotImplementedError.
    """
    if handler_type is not None:
        return handler_type(df)
    for df_type, df_handler in dispatch_dict.items():
        if isinstance(df, df_type):
            return df_handler(df)
    else:
        raise NotImplementedError(f"Unsupported DataFrame type: {type(df)}")


__all__.append("dispatch_dict")
__all__.append("get_handler")
