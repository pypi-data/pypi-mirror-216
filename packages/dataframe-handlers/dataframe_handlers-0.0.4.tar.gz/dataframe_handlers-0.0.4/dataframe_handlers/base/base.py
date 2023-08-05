import abc
from typing import Optional, Sequence, Mapping, Collection, Union


class BaseDataFrameHandler(abc.ABC):
    def __init__(self, df):
        """
        Initialize DataFrameHandler.

        Args:
            df: DataFrame-like object to be handled.
        """
        self.df = df

    @abc.abstractmethod
    def get_unique(self, column: str, limit: Optional[int] = None) -> Collection:
        """
        Get unique values in a column of the DataFrame.

        Args:
            column: Name of the column.
            limit: Maximum number of unique values to return.

        Returns:
            Collection of unique values.
        """
        pass

    @abc.abstractmethod
    def get_value_counts(
        self,
        column: str,
        limit: Optional[int] = None,
    ) -> Mapping[str, int]:
        """
        Count the occurrences of each value in a column of the DataFrame.

        Args:
            column: Name of the column.
            limit: Maximum number of value counts to return.

        Returns:
            (value, count) Mapping
        """
        pass

    @abc.abstractmethod
    def get_data_range(self, column: str) -> Sequence:
        """
        Get the minimum and maximum values in a column of the DataFrame.

        Args:
            column: Name of the column.

        Returns:
            Sequence containing the minimum and maximum values.
        """
        pass

    @abc.abstractmethod
    def get_missing_filter(self, column: str) -> Sequence[bool]:
        """
        Filter the DataFrame based on missing values in a column.

        Args:
            column: Name of the column.

        Returns:
            Boolean Series indicating missing values.
        """
        pass

    @abc.abstractmethod
    def get_value_filter(
        self,
        column: str,
        values: list,
        invert: bool = False,
    ) -> Sequence[bool]:
        """
        Filter the DataFrame based on specified values in a column.

        Args:
            column: Name of the column.
            values: List of values to filter on.
            invert: Flag indicating whether to invert the filter.

        Returns:
            Boolean Series indicating the filtered rows.
        """
        pass

    @abc.abstractmethod
    def get_columns(self) -> Collection[str]:
        pass

    @abc.abstractmethod
    def get_numeric_columns(self) -> Collection[str]:
        pass

    @abc.abstractmethod
    def get_column_types(
        self,
        default_str: bool = True,
    ) -> Mapping[str, Union[object, type, str]]:
        """
        Get the types of columns in the DataFrame.

        Args:
            default_str: If not numeric or bool, default to str.

        Returns:
            Dictionary mapping column names to their types.
        """
        pass
