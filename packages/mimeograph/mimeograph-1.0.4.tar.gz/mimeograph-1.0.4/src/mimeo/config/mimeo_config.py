"""The Mimeo Configuration module.

It contains classes representing Mimeo Configuration components at all levels.
All of them are Data Transfer Objects:
    * MimeoConfigFactory
        A factory class to instantiate a MimeoConfig.
    * MimeoDTO
        A superclass for all Mimeo configuration DTOs
    * MimeoConfig
        A MimeoDTO class representing Mimeo Configuration
    * MimeoOutput
        A MimeoDTO class representing Mimeo Output Details
    * MimeoTemplate
        A MimeoDTO class representing Mimeo Template
    * MimeoModel
        A MimeoDTO class representing Mimeo Model
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import xmltodict

from mimeo.config import constants as cc
from mimeo.config.exc import (InvalidIndentError, InvalidMimeoConfigError,
                              InvalidMimeoModelError,
                              InvalidMimeoTemplateError, InvalidVarsError,
                              MimeoConfigurationNotFoundError,
                              MissingRequiredPropertyError,
                              UnsupportedMimeoConfigSourceError,
                              UnsupportedPropertyValueError)
from mimeo.logging import setup_logging

# setup logging when mimeo is used as a python library
setup_logging()


class MimeoConfigFactory:
    """A factory class to instantiate a MimeoConfig.

    Methods
    -------
    parse(source: dict | str) -> MimeoConfig
        Instantiate MimeoConfig from a source configuration.
    parse_source(source: str) -> dict
        Parse a Mimeo Configuration to a source dict.
    """

    @classmethod
    def parse(
            cls,
            source: dict | str,
    ) -> MimeoConfig:
        """Instantiate MimeoConfig from a source configuration.

        It uses internal methods to instantiate Mimeo Config depending on source type.

        Parameters
        ----------
        source : dict | str
            A source configuration

        Returns
        -------
        MimeoConfig
            A parsed MimeoConfig instance

        Raises
        ------
        UnsupportedMimeoConfigSourceError
            If the source is neither a dict nor str value
        """
        if isinstance(source, str):
            source = cls.parse_source(source)
        if not isinstance(source, dict):
            raise UnsupportedMimeoConfigSourceError(source)

        return MimeoConfig(source)

    @classmethod
    def parse_source(
            cls,
            source: str,
    ) -> dict:
        """Parse a Mimeo Configuration to a source dict.

        It uses internal methods to parse Mimeo Configuration depending on source value.

        Parameters
        ----------
        source : str
            A source configuration

        Returns
        -------
        dict
            A parsed source Mimeo Configuration ready to be used in MimeoConfig
            initialization.
        """
        if cls._is_file_path(source):
            source = cls._parse_source_from_file(source)
        else:
            source = cls._parse_source_from_str(source)
        return source

    @staticmethod
    def _is_file_path(
            source: str,
    ) -> bool:
        """Verify if the Mimeo Configuration source is a file path.

        Parameters
        ----------
        source : str
            A Mimeo Configuration source

        Returns
        -------
        bool
            True if the source is a file path. Otherwise, False.
        """
        return bool(re.match(r"([a-zA-Z0-9\s_/\\.\-\(\):])+(.json|.xml)$", source))

    @classmethod
    def _parse_source_from_file(
            cls,
            config_path: str,
    ) -> dict:
        """Parse a Mimeo Configuration file to a source dict.

        Parameters
        ----------
        config_path : str
            A source config file path

        Returns
        -------
        dict
            A parsed source Mimeo Configuration ready to be used in MimeoConfig
            initialization.
        """
        with Path(config_path).open() as config_file:
            if config_path.endswith(".json"):
                config = json.load(config_file)
            elif config_path.endswith(".xml"):
                config = cls._parse_source_from_str(config_file.read())
        return config

    @classmethod
    def _parse_source_from_str(
            cls,
            source: str,
    ) -> dict:
        """Parse a string Mimeo Configuration to a source dict.

        Parameters
        ----------
        source : str
            A source string to parse

        Returns
        -------
        dict
            A parsed source Mimeo Configuration ready to be used in MimeoConfig
            initialization.
        """
        parsed_source = xmltodict.parse(source)
        if cc.CONFIG_XML_ROOT_NAME not in parsed_source:
            source_key = list(parsed_source.keys())[0]
            raise MimeoConfigurationNotFoundError(source_key)
        parsed_source = parsed_source[cc.CONFIG_XML_ROOT_NAME]
        return cls._parse_source_values(parsed_source)

    @classmethod
    def _parse_source_values(
            cls,
            source_node: None | str | bool | int | float | dict | list,
    ) -> None | str | bool | int | float | dict | list:
        """Parse source values.

        This method recursively parses result of parsing XML to dict.

        Parameters
        ----------
        source_node : None | str | bool | int | float | dict | list
            An XML Mimeo Configuration's node parsed to dict

        Returns
        -------
        None | str | bool | int | float | dict | list
            An XML Mimeo Configuration's node with parsed nested values.
        """
        if isinstance(source_node, str):
            return cls._parse_str_source_value(source_node)
        if isinstance(source_node, list):
            return cls._parse_list_source_value(source_node)
        if isinstance(source_node, dict):
            return cls._parse_dict_source_value(source_node)
        return None

    @classmethod
    def _parse_str_source_value(
            cls,
            source_node: str,
    ) -> bool | float | int | str:
        """Parse a string value.

        This method returns boolean values for 'true' and 'false' strings and casts
        to float or int numeric ones. Otherwise, returns a source value.

        Parameters
        ----------
        source_node : str
            An XML Mimeo Configuration's node

        Returns
        -------
        bool | float | int | str
            A parsed string value

        Examples
        --------
        MimeoDTO._parse_str_source_value('true')
        -> True

        MimeoDTO._parse_str_source_value('false')
        -> False

        MimeoDTO._parse_str_source_value('1.5')
        -> 1.5

        MimeoDTO._parse_str_source_value('1')
        -> 1

        MimeoDTO._parse_str_source_value('value')
        -> 'value'
        """
        if source_node == "true":
            return True
        if source_node == "false":
            return False
        if source_node.replace("-", "").isnumeric():
            return int(source_node)
        if re.sub(r"[-\.]", "", source_node).isnumeric():
            return float(source_node)
        return source_node

    @classmethod
    def _parse_list_source_value(
            cls,
            source_node: list,
    ) -> list:
        """Parse a list value.

        This method parses all list items.

        Parameters
        ----------
        source_node : list
            An XML Mimeo Configuration's node

        Returns
        -------
        list
            A list with parsed items

        Examples
        --------
        MimeoDTO._parse_list_source_value(['true', 'false', '1.5', '1', 'value'])
        -> [True, False, 1.5, 1, 'value']
        """
        return [cls._parse_source_values(value) for value in source_node]

    @classmethod
    def _parse_dict_source_value(
            cls,
            source_node: dict,
    ) -> dict:
        """Parse a dict value.

        This method parses all dict values. Additionally, it applies a specific logic
        for Mimeo Templates and random_item Mimeo Util. As XML Mimeo Configuration needs
        a template node in templates, it assigns them to the "_templates_" key (moves
        one level up). Similar modification is made for items of the random_item Mimeo
        Util.

        Parameters
        ----------
        source_node : dict
            An XML Mimeo Configuration's node

        Returns
        -------
        dict
            A dict with parsed values

        Examples
        --------
        MimeoDTO._parse_dict_source_value({
            'SomeField1': 'true',
            'SomeField2': 'false',
            'SomeField3': '1.5',
            'SomeField4': '1',
            'SomeField5': 'value',
        })
        -> {
            'SomeField1': True,
            'SomeField2': False,
            'SomeField3': 1.5,
            'SomeField4': 1,
            'SomeField5': 'value',
        }
        """
        for key, value in source_node.items():
            if key == cc.TEMPLATES_KEY:
                cls._flatten_list(
                    source_node,
                    cc.TEMPLATES_KEY,
                    cc.TEMPLATES_XML_TEMPLATE_TAG)
            elif (key == cc.MODEL_MIMEO_UTIL_KEY and
                  value is not None and
                  value.get(cc.MODEL_MIMEO_UTIL_NAME_KEY) == "random_item"):
                cls._flatten_list(
                    source_node[key],
                    "items",
                    "item")
            else:
                source_node[key] = cls._parse_source_values(value)

        return source_node

    @classmethod
    def _flatten_list(
            cls,
            source_node: str | dict | list,
            key: str,
            child_key: str,
    ):
        """Move child node value one level up to a list.

        Parameters
        ----------
        source_node : str | dict | list
            An XML Mimeo Configuration's node
        key : str
            A parent key to being reassigned
        child_key : str
            A child key to take value from

        Examples
        --------
        MimeoDTO._parse_dict_source_value({
            '_templates_': None,
        })
        -> {
            '_templates_': [],
        }

        MimeoDTO._parse_dict_source_value({
            '_templates_': {
                '_template_' : {
                    'SomeField': 'true',
                },
            }
        })
        -> {
            '_templates_': [
                {
                    'SomeField': 'true',
                },
            ],
        }

        MimeoDTO._parse_dict_source_value({
            '_templates_': {
                '_template_' : [
                    {
                        'SomeField': 'true',
                    },
                    {
                        'SomeField': 'false',
                    },
                ],
            },
        })
        -> {
            '_templates_': [
               {
                   'SomeField': 'true',
               },
               {
                   'SomeField': 'false',
               },
            ],
        }

        MimeoDTO._parse_dict_source_value({
            '_name': 'random_item',
            'items': {
                'item': [
                    'value',
                    1,
                    True
                ]
            }
        })
        -> {
            '_name': 'random_item',
            'items': [
                'value',
                1,
                True
            ]
        }
        """
        value = source_node[key]
        if value is None:
            source_node[key] = []
        elif isinstance(value, list):
            source_node[key] = cls._parse_source_values(value)
        else:
            templates = source_node[key].get(child_key)
            if isinstance(templates, (str, dict)):
                source_node[key] = [cls._parse_source_values(templates)]
            elif isinstance(templates, list):
                source_node[key] = cls._parse_source_values(templates)
            else:
                source_node[key] = cls._parse_source_values(value)


class MimeoDTO:
    """A superclass for all Mimeo configuration DTOs.

    It is meant to store a source dictionary for logging purposes.

    Methods
    -------
    __str__() -> str
        Return the stringified source dictionary of a DTO.
    """

    def __init__(
            self, source: dict,
    ):
        """Initialize MimeoDTO class.

        Parameters
        ----------
        source : dict
            The source dictionary for a Mimeo DTO
        """
        self._source: dict = source

    def __str__(
            self,
    ) -> str:
        """Return the stringified source dictionary of a DTO."""
        return str(self._source)


class MimeoConfig(MimeoDTO):
    """A MimeoDTO class representing Mimeo Configuration.

    It is a python representation of a Mimeo Configuration file / dictionary.

    output : MimeoOutput, default {}
        A Mimeo Output Details settings
    vars : dict, default {}
        A Mimeo Configuration vars setting
    templates : list
        A Mimeo Templates setting
    """

    def __init__(
            self,
            config: dict,
    ):
        """Initialize MimeoConfig class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        config : dict
            A source config dictionary
        """
        super().__init__(config)
        self.output: MimeoOutput = MimeoOutput(config.get(cc.OUTPUT_KEY, {}))
        self.vars: dict = self._get_vars(config)
        self.templates: list[MimeoTemplate] = self._get_templates(config)

    @classmethod
    def _get_vars(
            cls,
            config: dict,
    ) -> dict:
        """Extract variables from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        variables : dict
            Customized variables or an empty dictionary

        Raises
        ------
        InvalidVarsError
            If (1) the vars key does not point to a dictionary or
            (2) some variable's name does not start with a letter,
            is not SNAKE_UPPER_CASE with possible digits or
            (3) some variable's value points to non-atomic value nor Mimeo Util
        """
        variables = config.get(cc.VARS_KEY, {})
        if not isinstance(variables, dict):
            raise InvalidVarsError(InvalidVarsError.Code.ERR_1, vars=variables)
        for var, val in variables.items():
            if isinstance(val, (list, dict)) and not cls._is_mimeo_util_object(val):
                raise InvalidVarsError(InvalidVarsError.Code.ERR_2, var=var)
            if not re.match(r"^[A-Z][A-Z_0-9]*$", var):
                raise InvalidVarsError(InvalidVarsError.Code.ERR_3, var=var)
        return variables

    @classmethod
    def _get_templates(
            cls,
            config: dict,
    ) -> list[MimeoTemplate]:
        """Extract Mimeo Templates from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        list[MimeoTemplate]
            A Mimeo Templates list

        Raises
        ------
        InvalidMimeoConfigError
            If (1) the source dictionary does not include the _templates_ key or
            (2) the _templates_ key does not point to a list
        """
        templates = config.get(cc.TEMPLATES_KEY)
        if templates is None:
            raise InvalidMimeoConfigError(InvalidMimeoConfigError.Code.ERR_1,
                                          config=config)
        if not isinstance(templates, list):
            raise InvalidMimeoConfigError(InvalidMimeoConfigError.Code.ERR_2,
                                          config=config)
        return [MimeoTemplate(template)
                for template in config.get(cc.TEMPLATES_KEY)]

    @classmethod
    def _is_mimeo_util_object(
            cls,
            obj: dict,
    ) -> bool:
        """Verify if the object is a Mimeo Util.

        Parameters
        ----------
        obj : dict
            An object to verify

        Returns
        -------
        bool
            True if the object is a dictionary having only one key: _mimeo_util.
            Otherwise, False.
        """
        return (isinstance(obj, dict) and
                len(obj) == 1 and
                cc.MODEL_MIMEO_UTIL_KEY in obj)


class MimeoOutput(MimeoDTO):
    """A MimeoDTO class representing Mimeo Output Details.

    It is a python representation of a Mimeo Output Details configuration node.

    Attributes
    ----------
    direction : str, default 'file'
        The configured output direction
    format : str, default 'xml'
        A Mimeo Configuration output format setting
    xml_declaration : bool, default None
        A Mimeo Configuration xml declaration setting
    indent : int, default 0
        A Mimeo Configuration indent setting
    directory_path : str, default 'mimeo-output'
        The configured file output directory
    file_name : str, default 'mimeo-output-{}.{output_format}'
        The configured file output file name template
    method : str, default POST
        The configured http output request method
    protocol : str, default 'http'
        The configured http output protocol
    host : str
        The configured http output host
    port : str
        The configured http output port
    endpoint : str
        The configured http output endpoint
    username : str
        The configured http output username
    password : str
        The configured http output password
    """

    def __init__(
            self,
            output: dict,
    ):
        """Initialize MimeoOutput class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        output : dict
            A source config output details dictionary
        """
        super().__init__(output)
        self.direction: str = self._get_direction(output)
        self._validate_output(self.direction, output)
        self.format: str = self._get_format(output)
        self.xml_declaration: bool = self._get_xml_declaration(output, self.format)
        self.indent: int = self._get_indent(output)
        self.directory_path: str = self._get_directory_path(self.direction, output)
        self.file_name: str = self._get_file_name(self.direction, output, self.format)
        self.method: str = self._get_method(self.direction, output)
        self.protocol: str = self._get_protocol(self.direction, output)
        self.host: str = self._get_host(self.direction, output)
        self.port: int = self._get_port(self.direction, output)
        self.endpoint: str = self._get_endpoint(self.direction, output)
        self.username: str = self._get_username(self.direction, output)
        self.password: str = self._get_password(self.direction, output)

    @staticmethod
    def _get_direction(
            output: dict,
    ) -> str:
        """Extract output direction from the source dictionary.

        Parameters
        ----------
        output : dict
            A source config output details dictionary

        Returns
        -------
        direction : str
            The configured output direction

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured output direction is not supported
        """
        direction = output.get(cc.OUTPUT_DIRECTION_KEY, cc.OUTPUT_DIRECTION_FILE)
        if direction not in cc.SUPPORTED_OUTPUT_DIRECTIONS:
            raise UnsupportedPropertyValueError(
                cc.OUTPUT_DIRECTION_KEY,
                direction,
                cc.SUPPORTED_OUTPUT_DIRECTIONS)
        return direction

    @staticmethod
    def _get_format(
            config: dict,
    ) -> str:
        """Extract an output format from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        output_format : str
            The customized output format or 'xml' by default

        Raises
        ------
        UnsupportedPropertyValueError
            If the customized output format is not supported
        """
        output_format = config.get(cc.OUTPUT_FORMAT_KEY, cc.OUTPUT_FORMAT_XML)
        if output_format not in cc.SUPPORTED_OUTPUT_FORMATS:
            raise UnsupportedPropertyValueError(
                cc.OUTPUT_FORMAT_KEY,
                output_format,
                cc.SUPPORTED_OUTPUT_FORMATS)
        return output_format

    @staticmethod
    def _get_xml_declaration(
            config: dict,
            output_format: str,
    ) -> bool | None:
        """Extract an XML declaration setting from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary
        output_format : str
            The configured output format

        Returns
        -------
        bool | None
            The configured XML declaration setting when the output format is 'xml'.
            Otherwise, None. If the 'xml_declaration' setting is missing returns
            False by default.
        """
        if output_format == cc.OUTPUT_FORMAT_XML:
            return config.get(cc.OUTPUT_XML_DECLARATION_KEY, False)
        return None

    @staticmethod
    def _get_indent(
            config: dict,
    ) -> int:
        """Extract an indent value from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        indent : int
            The customized indent or 0 by default

        Raises
        ------
        InvalidIndentError
            If the customized indent is lower than zero
        """
        indent = config.get(cc.OUTPUT_INDENT_KEY, 0)
        if indent < 0:
            raise InvalidIndentError(indent)
        return indent

    @staticmethod
    def _get_directory_path(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an output directory path from the source dictionary.

        It is extracted only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured output directory path when the output direction is 'file'.
            Otherwise, None. If the 'directory_path' setting is missing returns
            'mimeo-output' by default.
        """
        if direction == cc.OUTPUT_DIRECTION_FILE:
            return output.get(cc.OUTPUT_DIRECTORY_PATH_KEY, "mimeo-output")
        return None

    @staticmethod
    def _get_file_name(
            direction: str,
            output: dict,
            output_format: str,
    ) -> str | None:
        """Generate an output file name template based on the source dictionary.

        It is generated only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary
        output_format : str
            The configured output format

        Returns
        -------
        str | None
            The configured output file name template when the output direction is
            'file'. Otherwise, None. If the 'file_name' setting is missing returns
            'mimeo-output-{}.{output_format}' by default.
        """
        if direction == cc.OUTPUT_DIRECTION_FILE:
            file_name = output.get(cc.OUTPUT_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"
        return None

    @staticmethod
    def _get_method(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP request method from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        method: str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'method' setting is missing returns
            'POST' by default.

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured request method is not supported
        """
        method = None
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            method = output.get(cc.OUTPUT_METHOD_KEY, cc.OUTPUT_HTTP_REQUEST_POST)
            if method not in cc.SUPPORTED_REQUEST_METHODS:
                raise UnsupportedPropertyValueError(
                    cc.OUTPUT_METHOD_KEY,
                    method,
                    cc.SUPPORTED_REQUEST_METHODS)
        return method

    @staticmethod
    def _get_protocol(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP protocol from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'protocol' setting is missing returns
            'http' by default.

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured request protocol is not supported
        """
        protocol = None
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            protocol = output.get(cc.OUTPUT_PROTOCOL_KEY, cc.OUTPUT_PROTOCOL_HTTP)
            if protocol not in cc.SUPPORTED_REQUEST_PROTOCOLS:
                raise UnsupportedPropertyValueError(
                    cc.OUTPUT_PROTOCOL_KEY,
                    protocol,
                    cc.SUPPORTED_REQUEST_PROTOCOLS)
        return protocol

    @staticmethod
    def _get_host(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP host from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP host when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_HOST_KEY)
        return None

    @staticmethod
    def _get_port(
            direction: str,
            output: dict,
    ) -> int | None:
        """Extract an HTTP port from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        int | None
            The configured HTTP port when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_PORT_KEY)
        return None

    @staticmethod
    def _get_endpoint(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP endpoint from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_ENDPOINT_KEY)
        return None

    @staticmethod
    def _get_username(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract a username from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured username when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_USERNAME_KEY)
        return None

    @staticmethod
    def _get_password(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract a password from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured password when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_PASSWORD_KEY)
        return None

    @staticmethod
    def _validate_output(
            direction: str,
            output: dict,
    ) -> None:
        """Validate output details in the source dictionary.

        The validation is being done according to the configured output
        direction.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Raises
        ------
        MissingRequiredPropertyError
            If the output details doesn't include all required settings
            for the direction
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            missing_details = []
            for detail in cc.REQUIRED_HTTP_DETAILS:
                if detail not in output:
                    missing_details.append(detail)
            if len(missing_details) > 0:
                raise MissingRequiredPropertyError(missing_details)


class MimeoTemplate(MimeoDTO):
    """A MimeoDTO class representing Mimeo Template.

    It is a python representation of a Mimeo Template configuration node.

    Attributes
    ----------
    count : int
        A configured count of the Mimeo Template
    model : MimeoModel
        A configured model of the Mimeo Template
    """

    def __init__(
            self,
            template: dict,
    ):
        """Initialize MimeoTemplate class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        template : dict
            A source config template dictionary
        """
        super().__init__(template)
        self._validate_template(template)
        self.count: int = template.get(cc.TEMPLATES_COUNT_KEY)
        self.model: MimeoModel = MimeoModel(template.get(cc.TEMPLATES_MODEL_KEY))

    @staticmethod
    def _validate_template(
            template: dict,
    ) -> None:
        """Validate template in the source dictionary.

        Parameters
        ----------
        template : dict
            A source config template dictionary

        Raises
        ------
        InvalidMimeoTemplateError
            If the source config doesn't include count or model properties
        """
        if cc.TEMPLATES_COUNT_KEY not in template:
            prop_name = "count"
            raise InvalidMimeoTemplateError(prop_name, template)
        if cc.TEMPLATES_MODEL_KEY not in template:
            prop_name = "model"
            raise InvalidMimeoTemplateError(prop_name, template)


class MimeoModel(MimeoDTO):
    """A MimeoDTO class representing Mimeo Model.

    It is a python representation of a Mimeo Model configuration node.

    Attributes
    ----------
    root_name : str
        A root node's tag
    root_data : dict
        A template data
    context_name : str
        A context name (root_name by default)
    """

    def __init__(
            self,
            model: dict,
    ):
        """Initialize MimeoModel class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        model : dict
            A source config model dictionary
        """
        super().__init__(model)
        self.root_name: str = MimeoModel._get_root_name(model)
        self.root_data: dict = model.get(self.root_name)
        self.context_name: str = MimeoModel._get_context_name(model, self.root_name)

    @staticmethod
    def _get_root_name(
            model: dict,
    ) -> str:
        """Extract a root name from the source dictionary.

        Parameters
        ----------
        model : dict
            A source config model dictionary

        Returns
        -------
        str
            The configured root node's tag

        Raises
        ------
        InvalidMimeoModelError
            If the source config has no or more than one root nodes
        """
        model_keys = list(filter(MimeoModel._is_not_configuration_key, iter(model)))
        if len(model_keys) == 0:
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_1, model=model)
        if len(model_keys) > 1:
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_2, model=model)
        return model_keys[0]

    @staticmethod
    def _get_context_name(
            model: dict,
            root_name: str,
    ) -> str:
        """Extract a context name from the source dictionary.

        Parameters
        ----------
        model : dict
            A source config model dictionary
        root_name : str
            The configured root node's tag

        Returns
        -------
        str
            The configured context name.
            If the 'context' setting is missing returns root name by default

        Raises
        ------
        InvalidMimeoModelError
            If the source config has a context name not being a string value
        """
        context_name = model.get(cc.MODEL_CONTEXT_KEY, root_name)
        if not isinstance(context_name, str):
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_3, model=model)
        return context_name

    @staticmethod
    def _is_not_configuration_key(
            dict_key: str,
    ) -> bool:
        """Verify if the dictionary key is a configuration one.

        Parameters
        ----------
        dict_key : str
            A dictionary key to verify

        Returns
        -------
        bool
            True if the key is 'context', otherwise False
        """
        return dict_key not in [cc.MODEL_CONTEXT_KEY]
