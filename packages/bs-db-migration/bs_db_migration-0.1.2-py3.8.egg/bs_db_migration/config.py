import yaml

import sys
from bs_db_migration.logger.logger import Logger

log_debug = Logger.get("config", Logger.Level.DEBUG, sys.stdout).debug
log_error = Logger.get("config", Logger.Level.ERROR, sys.stderr).error

from enum import Enum


class ConfigDBType(Enum):
    MSSQL = "mssql"
    POSTGRES = "postgres"


class Configuration:
    CONFIG_DATA: dict = {}

    def __init__(self, config_yaml_file=None, config_data=None):
        Configuration.CONFIG_DATA: dict = {}
        try:
            if config_yaml_file:
                with open(config_yaml_file) as config_file:
                    Configuration.CONFIG_DATA = yaml.load(
                        config_file, Loader=yaml.FullLoader
                    )
            elif config_data:
                Configuration.CONFIG_DATA = config_data
            else:
                raise Exception("No configuration data")

        except Exception as ex:
            Configuration.CONFIG_DATA = {}
            raise Exception("No configuration data found")

    @classmethod
    def get(cls, key):
        return cls.CONFIG_DATA.get(key, None)

    @classmethod
    def db_info(cls, db_type: ConfigDBType):
        try:
            config_data = cls.CONFIG_DATA.get("db_connection").get(db_type.value, None)
        except Exception as ex:
            log_error(f"invalid configuration: \n{ex}")
            config_data = None

        return config_data if config_data != None else None

    @classmethod
    def migration_info(cls):
        try:
            migration_config = cls.CONFIG_DATA.get("migration_info")
        except Exception as ex:
            log_error(f"invalid configuration: \n{ex}")
            migration_config = None

        return migration_config if migration_config != None else None

    @classmethod
    def get_connection_info(cls, connection_info):
        return (
            connection_info.get("host", ""),
            connection_info.get("port", ""),
            connection_info.get("id", ""),
            connection_info.get("pw", ""),
            connection_info.get("db", ""),
        )


if __name__ == "__main__":
    conf = Configuration(
        "/Users/jinwonchoi/github/bs_database_migration/config/config.yaml"
    )
    print(Configuration.get("mssql"))
