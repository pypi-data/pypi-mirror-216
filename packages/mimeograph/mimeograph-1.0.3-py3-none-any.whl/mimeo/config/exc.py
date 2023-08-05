"""The Mimeo Configuration Exceptions module.

It contains all custom exceptions related to Mimeo Configuration:
    * UnsupportedPropertyValueError
        A custom Exception class for unsupported properties' values.
    * MissingRequiredPropertyError
        A custom Exception class for missing required properties.
    * InvalidIndentError
        A custom Exception class for invalid indent configuration.
    * InvalidVarsError
        A custom Exception class for invalid vars' configuration.
    * InvalidVarsError.Code
        An Enumeration class for InvalidVarsError error codes.
    * InvalidMimeoModelError
        A custom Exception class for invalid model configuration.
    * InvalidMimeoModelError.Code
        An Enumeration class for InvalidMimeoModelError error codes.
    * InvalidMimeoTemplateError
        A custom Exception class for invalid template configuration.
    * InvalidMimeoConfigError
        A custom Exception class for invalid mimeo configuration.
    * InvalidMimeoConfigError.Code
        An Enumeration class for InvalidMimeoConfigError error codes.
    * UnsupportedMimeoConfigSourceError
        A custom Exception class for unsupported Mimeo Configuration source.
    * MimeoConfigurationNotFoundError
        A custom Exception class for no mimeo_configuration node in source xml.
"""


from __future__ import annotations

from enum import Enum
from typing import Any


class UnsupportedPropertyValueError(Exception):
    """A custom Exception class for unsupported properties' values.

    Raised when a Mimeo Configuration property points to a value
    not being supported by Mimeo.
    """

    def __init__(
            self,
            prop: str,
            val: str,
            supported_values: tuple,
    ):
        """Initialize UnsupportedPropertyValueError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        prop : str
            A property name
        val : str
            A property value
        supported_values : tuple
            A list of supported values for the property
        """
        super().__init__(f"Provided {prop} [{val}] is not supported! "
                         f"Supported values: [{', '.join(supported_values)}].")


class MissingRequiredPropertyError(Exception):
    """A custom Exception class for missing required properties.

    Raised when a Mimeo Configuration does not contain a required
    property.
    """

    def __init__(
            self,
            details: list,
    ):
        """Initialize MissingRequiredPropertyError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        details : list
            Missing details
        """
        details_str = ", ".join(details)
        super().__init__(f"Missing required fields in HTTP output details: "
                         f"{details_str}")


class InvalidIndentError(Exception):
    """A custom Exception class for invalid indent configuration.

    Raised when a configured indent is negative.
    """

    def __init__(
            self,
            indent: int,
    ):
        """Initialize InvalidIndentError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        indent : int
            A configured indent
        """
        super().__init__(f"Provided indent [{indent}] is negative!")


class InvalidVarsError(Exception):
    """A custom Exception class for invalid vars' configuration.

    Raised when vars are not configured properly.
    """

    class Code(Enum):
        """An Enumeration class for InvalidVarsError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for vars not being a dictionary
        ERR_2: str
            An error code for vars with non-atomic values
        ERR_2: str
            An error code for vars with not allowed characters
        """

        ERR_1: str = "NOT_A_DICT"
        ERR_2: str = "COMPLEX_VALUE"
        ERR_3: str = "INVALID_NAME"

    def __init__(
            self,
            code: InvalidVarsError.Code,
            **kwargs,
    ):
        """Initialize InvalidVarsError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidVarsError code.

        Parameters
        ----------
        code : InvalidVarsError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidVarsError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidVarsError.Code
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
            If the code argument is not InvalidVarsError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"vars property does not store an object: {details['vars']}"
        if code == cls.Code.ERR_2:
            return (f"Provided var [{details['var']}] is invalid "
                    f"(you can use ony atomic values and Mimeo Utils)!")
        if code == cls.Code.ERR_3:
            return (f"Provided var [{details['var']}] is invalid "
                    f"(you can use upper-cased name with underscore and digits, "
                    f"starting with a letter)!")

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class InvalidMimeoModelError(Exception):
    """A custom Exception class for invalid model configuration.

    Raised when a Mimeo Model is not configured properly.
    """

    class Code(Enum):
        """An Enumeration class for InvalidMimeoModelError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for missing root in the Mimeo Model
        ERR_2: str
            An error code for multiple roots in the Mimeo Model
        ERR_2: str
            An error code for invalid context name in Mimeo Model
        """

        ERR_1: str = "MISSING_ROOT"
        ERR_2: str = "MULTIPLE_ROOTS"
        ERR_3: str = "INVALID_CONTEXT_NAME"

    def __init__(
            self,
            code: InvalidMimeoModelError.Code,
            **kwargs,
    ):
        """Initialize InvalidMimeoModelError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidMimeoModelError code.

        Parameters
        ----------
        code : InvalidMimeoModelError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidMimeoModelError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidMimeoModelError.Code
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
            If the code argument is not InvalidMimeoModelError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"No root data in Mimeo Model: {details['model']}"
        if code == cls.Code.ERR_2:
            return f"Multiple root data in Mimeo Model: {details['model']}"
        if code == cls.Code.ERR_3:
            return (f"Invalid context name in Mimeo Model (not a string value): "
                    f"{details['model']}")

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class InvalidMimeoTemplateError(Exception):
    """A custom Exception class for invalid template configuration.

    Raised when a Mimeo Template is not configured properly.
    """

    def __init__(
            self,
            property_name: str,
            template: dict,
    ):
        """Initialize InvalidMimeoTemplateError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        property_name : str
            A missing property
        template : dict
            A Mimeo Template
        """
        super().__init__(f"No {property_name} property in the Mimeo Template: "
                         f"{template}")


class InvalidMimeoConfigError(Exception):
    """A custom Exception class for invalid mimeo configuration.

    Raised when a Mimeo Configuration is not configured properly.
    """

    class Code(Enum):
        """An Enumeration class for InvalidMimeoConfigError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for missing templates in the Mimeo Configuration
        ERR_2: str
            An error code for invalid templates in the Mimeo Configuration
        """

        ERR_1: str = "MISSING_TEMPLATES"
        ERR_2: str = "NOT_AN_ARRAY"

    def __init__(
            self,
            code: InvalidMimeoConfigError.Code,
            **kwargs,
    ):
        """Initialize InvalidMimeoConfigError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidMimeoConfigError code.

        Parameters
        ----------
        code : InvalidMimeoConfigError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidMimeoConfigError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidMimeoConfigError.Code
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
            If the code argument is not InvalidMimeoConfigError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"No templates in the Mimeo Config: {details['config']}"
        if code == cls.Code.ERR_2:
            return f"_templates_ property does not store an array: {details['config']}"

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class UnsupportedMimeoConfigSourceError(Exception):
    """A custom Exception class for unsupported Mimeo Configuration source.

    Raised when an XML Mimeo Configuration's source is neither a dict nor str.
    """

    def __init__(
            self,
            source: Any,
    ):
        """Initialize UnsupportedMimeoConfigSourceError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        source : Any
            An actual root name
        """
        super().__init__(f"Mimeo Configuration source [{source}] is unsupported. "
                         "Use a file path, stringified configuration or a dictionary.")


class MimeoConfigurationNotFoundError(Exception):
    """A custom Exception class for no mimeo_configuration node in source xml.

    Raised when an XML Mimeo Configuration's root node is not <mimeo_configuration/>.
    """

    def __init__(
            self,
            root_name: str,
    ):
        """Initialize MimeoConfigurationNotFoundError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        root_name : str
            An actual root name
        """
        super().__init__(f"<mimeo_configuration/> not found! {root_name} is not "
                         f"a proper Mimeo Configuration root node.")
