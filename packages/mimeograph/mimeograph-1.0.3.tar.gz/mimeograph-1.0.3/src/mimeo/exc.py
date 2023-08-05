"""The Mimeograph Exceptions module.

It contains all custom exceptions related to the highest Mimeograph level:
    * NotRunningMimeograph
        A custom Exception class for not running Mimeograph instance.
"""


from __future__ import annotations


class NotRunningMimeographError(Exception):
    """A custom Exception class for not running Mimeograph instance.

    Raised when using submit() method without running Mimeograph first.
    """

    def __init__(
            self,
    ):
        """Initialize NotRunningMimeograph exception with details.

        Extends Exception constructor with a constant message.
        """
        super().__init__("The Mimeograph instance is not running!")
