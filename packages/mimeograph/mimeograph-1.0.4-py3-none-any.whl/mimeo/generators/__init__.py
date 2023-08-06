"""The Mimeo Generators package.

It contains modules supporting the Mimeo Config output formats:
* generator
    The Mimeo Generator module.
* generator_factory
    The Mimeo Generator Factory module.
* json_generator
    The Mimeo JSON Generator module.
* xml_generator
    The Mimeo XML Generator module.
* exc
    The Mimeo Generators Exceptions module.

This package exports the following classes:
* Generator:
    An abstract class for data generators in Mimeo.
* GeneratorFactory:
    A Factory class instantiating a Generator based on Mimeo Config.
* JSONGenerator:
    A Generator implementation producing data in the JSON format.
    Corresponds to the 'json' output format
* XMLGenerator:
    A Generator implementation producing data in the XML format.
    Corresponds to the 'xml' output format

To use this package, simply import the desired class:
    from mimeo.generators import GeneratorFactory
    from mimeo.generators.exc import UnsupportedStructureError
"""
from .generator import Generator
from .json_generator import JSONGenerator
from .xml_generator import XMLGenerator
from .generator_factory import GeneratorFactory

__all__ = ["Generator", "JSONGenerator", "XMLGenerator", "GeneratorFactory"]
