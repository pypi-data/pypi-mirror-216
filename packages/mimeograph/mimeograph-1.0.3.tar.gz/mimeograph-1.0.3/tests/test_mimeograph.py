import shutil
import time
from pathlib import Path
from xml.etree import ElementTree as ElemTree

import pytest

from mimeo import Mimeograph
from mimeo.config import MimeoConfigFactory
from mimeo.exc import NotRunningMimeographError
from tests.utils import assert_throws


@pytest.fixture(autouse=True)
def _teardown():
    yield
    # Teardown
    shutil.rmtree("test_mimeograph-dir", ignore_errors=True)


def test_process_xml():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    Mimeograph.process(mimeo_config)
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file.readline() == "<SomeEntity>\n"
            assert file.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file.readline() == "</SomeEntity>\n"


def test_process_json():
    config = {
        "output": {
            "direction": "file",
            "format": "json",
            "indent": 4,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    Mimeograph.process(mimeo_config)
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.json"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == "{\n"
            assert file.readline() == '    "SomeEntity": {\n'
            assert file.readline() == '        "ChildNode1": 1,\n'
            assert file.readline() == '        "ChildNode2": "value-2",\n'
            assert file.readline() == '        "ChildNode3": true\n'
            assert file.readline() == "    }\n"
            assert file.readline() == "}"


def test_generate_xml():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)

    count = 0
    for data in Mimeograph.generate(mimeo_config):
        assert isinstance(data, ElemTree.Element)

        assert data.tag == "SomeEntity"
        assert data.attrib == {}
        assert len(list(data)) == 3  # number of children

        child = data.find("ChildNode1")
        assert child.tag == "ChildNode1"
        assert child.attrib == {}
        assert child.text == "1"
        assert len(list(child)) == 0  # number of children

        child = data.find("ChildNode2")
        assert child.tag == "ChildNode2"
        assert child.attrib == {}
        assert child.text == "value-2"
        assert len(list(child)) == 0  # number of children

        child = data.find("ChildNode3")
        assert child.tag == "ChildNode3"
        assert child.attrib == {}
        assert child.text == "true"
        assert len(list(child)) == 0  # number of children

        count += 1

    assert count == 10


def test_generate_xml_stringified():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)

    count = 0
    for data in Mimeograph.generate(mimeo_config, stringify=True):
        assert isinstance(data, str)

        assert data == ('<?xml version="1.0" encoding="utf-8"?>\n'
                        "<SomeEntity>\n"
                        "    <ChildNode1>1</ChildNode1>\n"
                        "    <ChildNode2>value-2</ChildNode2>\n"
                        "    <ChildNode3>true</ChildNode3>\n"
                        "</SomeEntity>\n")

        count += 1

    assert count == 10


def test_generate_json():
    config = {
        "output": {
            "direction": "file",
            "format": "json",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)

    count = 0
    for data in Mimeograph.generate(mimeo_config):
        assert isinstance(data, dict)

        assert data == {
            "SomeEntity": {
                "ChildNode1": 1,
                "ChildNode2": "value-2",
                "ChildNode3": True,
            },
        }
        count += 1

    assert count == 10


def test_generate_json_stringified():
    config = {
        "output": {
            "direction": "file",
            "format": "json",
            "indent": 4,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)

    count = 0
    for data in Mimeograph.generate(mimeo_config, stringify=True):
        assert isinstance(data, str)

        assert data == ("{\n"
                        '    "SomeEntity": {\n'
                        '        "ChildNode1": 1,\n'
                        '        "ChildNode2": "value-2",\n'
                        '        "ChildNode3": true\n'
                        "    }\n"
                        "}")

        count += 1

    assert count == 10


def test_consume_xml():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    data = Mimeograph.generate(mimeo_config, stringify=True)
    Mimeograph.consume(mimeo_config, data)
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file.readline() == "<SomeEntity>\n"
            assert file.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file.readline() == "</SomeEntity>\n"


def test_consume_json():
    config = {
        "output": {
            "direction": "file",
            "format": "json",
            "indent": 4,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    data = Mimeograph.generate(mimeo_config, stringify=True)
    Mimeograph.consume(mimeo_config, data)
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.json"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == "{\n"
            assert file.readline() == '    "SomeEntity": {\n'
            assert file.readline() == '        "ChildNode1": 1,\n'
            assert file.readline() == '        "ChildNode2": "value-2",\n'
            assert file.readline() == '        "ChildNode3": true\n'
            assert file.readline() == "    }\n"
            assert file.readline() == "}"


def test_submit_using_run_and_stop():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    mimeo = Mimeograph()
    mimeo.run()
    mimeo.submit(("xml-config", mimeo_config))
    mimeo.stop()
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file.readline() == "<SomeEntity>\n"
            assert file.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file.readline() == "</SomeEntity>\n"


def test_submit_as_context_manager():
    config = {
        "output": {
            "direction": "file",
            "format": "json",
            "indent": 4,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    with Mimeograph() as mimeo:
        mimeo.submit(("json-config", mimeo_config))
    assert Path("test_mimeograph-dir").exists()
    for i in range(1, 11):
        file_path = f"test_mimeograph-dir/output-{i}.json"
        assert Path(file_path).exists()

        with Path(file_path).open() as file:
            assert file.readline() == "{\n"
            assert file.readline() == '    "SomeEntity": {\n'
            assert file.readline() == '        "ChildNode1": 1,\n'
            assert file.readline() == '        "ChildNode2": "value-2",\n'
            assert file.readline() == '        "ChildNode3": true\n'
            assert file.readline() == "    }\n"
            assert file.readline() == "}"


@assert_throws(err_type=NotRunningMimeographError,
               msg="The Mimeograph instance is not running!")
def test_submit_when_non_running():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    mimeo = Mimeograph()
    mimeo.submit(("xml-config", mimeo_config))


def test_default_number_of_workers():
    assert Mimeograph()._consumer_workers > 4


def test_custom_number_of_workers():
    assert Mimeograph(workers=1)._consumer_workers == 1


def test_config_failed_at_generation_step():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "directory_path": "test_mimeograph-dir",
            "file_name": "output",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "Bolívar Soberano",  # Non-ascii character
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    with Mimeograph() as mimeo:
        mimeo.submit(("non-ascii-character-config", mimeo_config))
        time.sleep(0.05)
        assert mimeo._failed_configs == ["non-ascii-character-config"]
    assert not Path("test_mimeograph-dir").exists()


def test_config_failed_at_consuming_step():
    config = {
        "output": {
            "direction": "http",
            "format": "xml",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/documents",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    assert not Path("test_mimeograph-dir").exists()
    with Mimeograph() as mimeo:
        mimeo.submit(("no-connection-config", mimeo_config))
        time.sleep(0.05)
        assert mimeo._failed_configs == ["no-connection-config"]
    assert not Path("test_mimeograph-dir").exists()
