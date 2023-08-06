#!/usr/bin/env python3
"""Top-level package for zyme."""
# Core Library modules
import configparser
import json
import logging.config
import pickle
from importlib.resources import as_file, files

# Third party modules
import toml  # type: ignore
import yaml  # type: ignore

__title__ = "zyme"
__version__ = "0.1.5"
__author__ = "Stephen R A King"
__description__ = "placeholder"
__email__ = "sking.github@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Stephen R A King"


LOGGING_CONFIG = """
version: 1
disable_existing_loggers: False
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    stream: ext://sys.stdout
    formatter: basic
  file:
    class: logging.FileHandler
    level: DEBUG
    filename: zyme.log
    encoding: utf-8
    formatter: timestamp

formatters:
  basic:
    style: "{"
    format: "{levelname:s}:{name:s}:{message:s}"
  timestamp:
    style: "{"
    format: "{asctime} - {levelname} - {name} - {message}"

loggers:
  init:
    handlers: [console, file]
    level: DEBUG
    propagate: False
"""

logging.config.dictConfig(yaml.safe_load(LOGGING_CONFIG))
logger = logging.getLogger("init")

source_yaml = files("zyme.resources").joinpath("config.yaml")
with as_file(source_yaml) as _yaml_path:
    _yaml_text = _yaml_path.read_text()
    yaml_config = yaml.safe_load(_yaml_text)

source_json = files("zyme.resources").joinpath("config.json")
with as_file(source_json) as _json_path:
    _json_text = _json_path.read_text()
    json_config = json.loads(_json_text)

source_ini = files("zyme.resources").joinpath("config.ini")
with as_file(source_ini) as _ini_path:
    _ini_text = _ini_path.read_text()
    _ini = configparser.ConfigParser()
    _ini.optionxform = str  # type: ignore
    _ini.read_string(_ini_text)
    ini_config = {section: dict(_ini.items(section)) for section in _ini.sections()}

source_toml = files("zyme.resources").joinpath("config.toml")
with as_file(source_toml) as _toml_path:
    _toml_text = _toml_path.read_text()
    toml_config = toml.loads(_toml_text)

source_pickle = files("zyme.resources").joinpath("resource.pickle")
with as_file(source_pickle) as _pickle_file:
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
