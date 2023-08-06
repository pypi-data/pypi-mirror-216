import sys
from bs_db_migration.logger.logger import Logger

log_debug = Logger.get("type-mapping", Logger.Level.DEBUG, sys.stdout).debug
log_error = Logger.get("type-mapping", Logger.Level.ERROR, sys.stderr).error


class MS2PostgresTypeMapping:
    MAPPING_TABLE = {
        "bigint": ["bigint"],
        "binary": ["bytea"],
        "bit": ["boolean"],
        "char": ["char", "LENGTH"],
        "date": ["date"],
        "datetime": ["timestamp(3)"],
        "datetime2": ["timestamp", "PRECISION"],
        "decimal": ["decimal", "PRECISION", "SCALE"],
        "dec": ["dec", "PRECISION", "SCALE"],
        "double precision": ["double precision"],
        "float": ["float", "PRECISION"],
        "image": ["bytea"],
        "int": ["int"],
        "integer": ["integer"],
        "money": ["money"],
        "nchar": ["char", "LENGTH"],
        "ntext": ["text"],
        "numeric": ["numeric", "PRECISION", "SCALE"],
        "nvarchar": ["varchar", "LENGTH"],
        "nvarchar(max)": ["text"],
        "real": ["real"],
        "rowversion": ["bytea"],
        "smalldatetime": ["timestamp(0)"],
        "smallint": ["smallint"],
        "smallmoney": ["money"],
        "text": ["text"],
        "time": ["time", "PRECISION"],
        "timestamp": ["bytea"],
        "tinyint": ["smallint"],
        "uniqueidentifier": ["uuid"],
        "varbinary": ["bytea"],
        "varchar": ["varchar", "LENGTH"],
        "varchar(max)": ["text"],
        "xml": ["xml"],
    }

    @staticmethod
    def convert_type(column_info):
        convert_list = MS2PostgresTypeMapping.MAPPING_TABLE[column_info["TYPE_NAME"]]
        convert_list_len = len(convert_list)

        if convert_list_len == 1:
            return convert_list[0]
        elif convert_list_len == 2:
            return f"{convert_list[0]}({column_info[convert_list[1]]})"
        elif convert_list_len == 3:
            return f"{convert_list[0]}({column_info[convert_list[1]]},{column_info[convert_list[2]]})"
        else:
            raise Exception("Invalid MSSQL type")

    @staticmethod
    def convert_nuallable(column_info):
        return "" if column_info["IS_NULLABLE"] == "YES" else "NOT NULL"


class PostgresTypeMapping:
    @staticmethod
    def convert_type(column_type, column_size):
        if column_type == "VARCHAR":
            return f"{column_type}({column_size})" if column_size else "VARCHAR"
        else:
            return column_type

    @staticmethod
    def convert_nuallable(column_nullable):
        return "" if column_nullable in ["Yes", "Y"] else "NOT NULL"


if __name__ == "__main__":
    test_column_info = {
        "TABLE_QUALIFIER": "BSI4",
        "TABLE_OWNER": "dbo",
        "TABLE_NAME": "CUSTTABLE",
        "COLUMN_NAME": "TKR_LICENSEATTACHFILE",
        "DATA_TYPE": -9,
        "TYPE_NAME": "nvarchar",
        "PRECISION": 259,
        "LENGTH": 518,
        "SCALE": None,
        "RADIX": None,
        "NULLABLE": 0,
        "REMARKS": None,
        "COLUMN_DEF": "('')",
        "SQL_DATA_TYPE": -9,
        "SQL_DATETIME_SUB": None,
        "CHAR_OCTET_LENGTH": 518,
        "ORDINAL_POSITION": 183,
        "IS_NULLABLE": "NO",
        "SS_DATA_TYPE": 39,
    }

    print(MS2PostgresTypeMapping.convert_type(test_column_info))
