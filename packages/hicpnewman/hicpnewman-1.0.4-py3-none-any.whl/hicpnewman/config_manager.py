# DATACLASSES
from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ContextJson:
    status: str
    content: dict

@dataclass_json
@dataclass
class ContextCsv:
    status: str
    content: Optional[list[list[str]]]

@dataclass_json
@dataclass
class Collection:
    collection: ContextJson
    environment: ContextJson
    globals: ContextJson
    data: ContextCsv

@dataclass_json
@dataclass
class Flag:
    active: bool
    command: str
    

@dataclass_json
@dataclass
class Reporter:
    package: str
    export_path: str
    flags: list[Flag]

@dataclass_json
@dataclass
class DefaultEnvs:
    collection: ContextJson
    environment: ContextJson
    globals: ContextJson
    data: ContextCsv

@dataclass_json
@dataclass
class Newman:
    command: str
    flags: list[Flag]
    reporters: dict[str, Reporter]

@dataclass_json
@dataclass
class Config:
    collections: dict[str, Collection]
    newman: Newman
    default: DefaultEnvs

# CONFIG
import os
import json

config_file_path = os.path.join(os.path.dirname(__file__), 'config/config.json')
backup_file_path = os.path.join(os.path.dirname(__file__), 'config/config_backup.json')
default_file_path = os.path.join(os.path.dirname(__file__), 'config/config_default.json')

def backup_config():
    with open(config_file_path, "r") as config_file:
        data = json.load(config_file)
    with open(backup_file_path, 'w') as backup_file:
        json.dump(data, backup_file, indent=4)

def load_config():
    backup_config()
    with open(config_file_path, "r") as config_file:
        data = json.load(config_file)
    return Config.from_dict(data)

def save_config(updated_config):
    with open(config_file_path, 'w') as config_file:
        json.dump(updated_config.to_dict(), config_file, indent=4)

def reset_config():
    backup_config()
    with open(default_file_path, "r") as default_file:
        data = json.load(default_file)
    with open(config_file_path, 'w') as config_file:
        json.dump(data, config_file, indent=4)

def revert_config():
    with open(backup_file_path, "r") as backup_file:
        data = json.load(backup_file)
    with open(config_file_path, 'w') as config_file:
        json.dump(data, config_file, indent=4)
