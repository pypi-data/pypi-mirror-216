"""The Mimeo Configuration package.

It contains the following modules:
* mimeo_config
    The Mimeo Configuration module
* constants
    The Mimeo Configuration Constants module
* exc
    The Mimeo Configuration Exceptions module

The Mimeo Configuration package exports a class representing
root Mimeo Configuration component and a factory:
* MimeoConfig
    A MimeoDTO class representing Mimeo Configuration
* MimeoConfigFactory
    A factory class to instantiate a MimeoConfig

To use this package, simply import it:
    from mimeo.config import MimeoConfigFactory, MimeoConfig
    from mimeo.config import constants as cc
    from mimeo.config.exc import UnsupportedPropertyValueError
"""
from __future__ import annotations

from .mimeo_config import MimeoConfig, MimeoConfigFactory

__all__ = ["MimeoConfig", "MimeoConfigFactory"]
