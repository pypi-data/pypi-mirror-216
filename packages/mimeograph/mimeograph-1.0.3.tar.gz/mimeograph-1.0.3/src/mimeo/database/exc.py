"""The Mimeo Database Exceptions module.

It contains all custom exceptions related to Mimeo Context:
    * InvalidIndexError
        A custom Exception class for invalid row index.
    * InvalidSexError
        A custom Exception class for uninitialized context's iteration.
    * DataNotFoundError
        A custom Exception class for not found data.
    * DataNotFoundError.Code
        An Enumeration class for DataNotFoundError error codes.
    * OutOfStockError
        A custom Exception class for invalid special field's name.
    * DataNotFoundError.Code
        An Enumeration class for OutOfStockError error codes.
"""


from __future__ import annotations

from enum import Enum


class InvalidIndexError(Exception):
    """A custom Exception class for invalid row index.

    Raised while attempting to get data at row that does not exist.
    """

    def __init__(
            self,
            index: int,
            last_index: int,
    ):
        """Initialize InvalidIndexError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        index : int
            An invalid index
        last_index : str
            The last existing index
        """
        msg = f"Provided index [{index}] is out or the range: 0-{last_index}!"
        super().__init__(msg)


class InvalidSexError(Exception):
    """A custom Exception class for invalid sex.

    Raised when sex provided to filter forenames is not supported.
    """

    def __init__(
            self,
            supported_sex_list: tuple,
    ):
        """Initialize InvalidSexError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        supported_sex_list : int
            A list of supported sex values
        """
        super().__init__(f"Invalid sex (use {' / '.join(supported_sex_list)})!")


class DataNotFoundError(Exception):
    """A custom Exception class for not found data.

    Raised while attempting to filter data by a column's value that
    does not match any row.
    """

    class Code(Enum):
        """An Enumeration class for DataNotFoundError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for not found data
        ERR_2: str
            An error code for not found data depending on a custom param
        """

        ERR_1 = "NOT_FOUND"
        ERR_2 = "NOT_FOUND_FOR"

    def __init__(
            self,
            code: DataNotFoundError.Code,
            **kwargs,
    ):
        """Initialize DataNotFoundError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal DataNotFoundError code.

        Parameters
        ----------
        code : DataNotFoundError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: DataNotFoundError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : DataNotFoundError.Code
            An internal error code
        details : dict
            An error details

        Returns
        -------
        str
            A custom error message

        Raises
        ------
        ValueError
            If the code argument is not DataNotFoundError.Code enum
        """
        if code == cls.Code.ERR_1:
            return (f"Mimeo database doesn't contain a {details['data']} "
                    f"[{details['value']}].")
        if code == cls.Code.ERR_2:
            return (f"Mimeo database doesn't contain any {details['data']} of "
                    f"the provided {details['param_name']} [{details['param_val']}].")

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class OutOfStockError(Exception):
    """A custom Exception class for consuming all data.

    Raised while attempting to get next unique value when all were
    consumed already.
    """

    class Code(Enum):
        """An Enumeration class for OutOfStockError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for no more unique values
        ERR_2: str
            An error code for no more unique values depending on a custom param
        """

        ERR_1 = "NO_MORE_UNIQUE_VALUES"
        ERR_2 = "NO_MORE_UNIQUE_VALUES_FOR"

    def __init__(
            self,
            code: OutOfStockError.Code,
            **kwargs,
    ):
        """Initialize OutOfStockError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal OutOfStockError code.

        Parameters
        ----------
        code : OutOfStockError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: OutOfStockError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : OutOfStockError.Code
            An internal error code
        details : dict
            An error details

        Returns
        -------
        str
            A custom error message

        Raises
        ------
        ValueError
            If the code argument is not OutOfStockError.Code enum
        """
        if code == cls.Code.ERR_1:
            return (f"No more unique values, "
                    f"database contain only {details['num']} {details['data']}.")
        if code == cls.Code.ERR_2:
            return (f"No more unique values, "
                    f"database contain only {details['num']} {details['data']} of "
                    f"{details['param_val']}.")

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)
