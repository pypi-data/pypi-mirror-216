"""The Mimeo Utils Exceptions module.

It contains all custom exceptions related to Mimeo Utils:
    * InvalidMimeoUtilError
        A custom Exception class for an invalid Mimeo Util.
    * InvalidMimeoUtilError.Code
        An Enumeration class for InvalidMimeoUtilError error codes.
    * InvalidValueError
        A custom Exception class for an invalid value in Mimeo Util.
    * InvalidValueError.Code
        An Enumeration class for InvalidValueError error codes.
    * NotASpecialFieldError
        A custom Exception class for a field used as a special.
"""


from __future__ import annotations

from enum import Enum


class InvalidMimeoUtilError(Exception):
    """A custom Exception class for an invalid Mimeo Util.

    Raised when Mimeo Util node has missing _name property, or it
    does not match any Mimeo Util.
    """

    class Code(Enum):
        """An Enumeration class for InvalidMimeoUtilError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for a missing Mimeo Util name in configuration
        ERR_2: str
            An error code for an unsupported Mimeo Util
        """

        ERR_1: str = "MISSING_NAME"
        ERR_2: str = "UNSUPPORTED_MIMEO_UTIL"

    def __init__(
            self,
            code: InvalidMimeoUtilError.Code,
            **kwargs,
    ):
        """Initialize InvalidMimeoUtilError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidMimeoUtilError code.

        Parameters
        ----------
        code : InvalidMimeoUtilError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidMimeoUtilError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidMimeoUtilError.Code
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
            If the code argument is not InvalidMimeoUtilError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"Missing Mimeo Util name in configuration [{details['config']}]!"
        if code == cls.Code.ERR_2:
            return f"No such Mimeo Util [{details['name']}]!"

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class InvalidValueError(Exception):
    """A custom Exception class for an invalid value in Mimeo Util.

    Raised when Mimeo Util node is incorrectly parametrized.
    """

    class Code(Enum):
        """An Enumeration class for InvalidValueError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for a negative length in Mimeo Util configuration
        ERR_2: str
            An error code for a limit param lower than start
        ERR_3: str
            An error code for an invalid param type
        ERR_3: str
            An error code for an unsupported value
        """

        ERR_1: str = "NEGATIVE_LENGTH"
        ERR_2: str = "LIMIT_LOWER_THAN_START"
        ERR_3: str = "INVALID_TYPE"
        ERR_4: str = "UNSUPPORTED_VALUE"

    def __init__(
            self,
            code: InvalidValueError.Code,
            **kwargs,
    ):
        """Initialize InvalidValueError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidValueError code.

        Parameters
        ----------
        code : InvalidValueError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidMimeoUtilError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidValueError.Code
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
            If the code argument is not InvalidValueError.Code enum
        """
        if code == cls.Code.ERR_1:
            msg = (f"The {details['util']} Mimeo Util cannot be parametrized with "
                   f"negative length [{details['length']}] value")
        elif code == cls.Code.ERR_2:
            msg = (f"The {details['util']} Mimeo Util cannot be parametrized with "
                   f"limit [{details['limit']}] lower than start [{details['start']}]")
        elif code == cls.Code.ERR_3:
            msg = (f"The {details['util']} Mimeo Util require a {details['type']} "
                   f"value for the {details['param_name']} parameter and was: "
                   f"[{details['param_val']}].")
        elif code == cls.Code.ERR_4:
            msg = (f"The {details['util']} Mimeo Util does not support a value "
                   f"[{details['value']}]. "
                   f"Supported values are: {', '.join(details['supported_values'])}.")
        else:
            msg = f"Provided error code is not a {cls.__name__}.Code enum!"
            raise ValueError(msg)
        return msg


class NotASpecialFieldError(Exception):
    """A custom Exception class for a field used as a special.

    Raised while attempting to retrieve special field name when it is
    not a special one.
    """

    def __init__(
            self,
            field_name: str,
    ):
        """Initialize NotASpecialFieldError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_name : str
            A field name
        """
        msg = f"Provided field [{field_name}] is not a special one (use {':NAME:'})!"
        super().__init__(msg)
