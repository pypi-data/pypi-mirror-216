import pymssql as ms
import psycopg2 as pg2
import psycopg2.extras as extras
from bs_db_migration.config import Configuration, ConfigDBType
from bs_db_migration.common.debug import print_execution_time
import datetime
import time

import sys
from bs_db_migration.logger.logger import Logger

log_info = Logger.get("bs_db_migration", Logger.Level.INFO, sys.stdout).info
log_debug = Logger.get("bs_db_migration", Logger.Level.DEBUG, sys.stdout).debug
log_error = Logger.get("bs_db_migration", Logger.Level.ERROR, sys.stderr).error

from bs_db_migration.ms2postgres_type_mapping import (
    MS2PostgresTypeMapping,
    PostgresTypeMapping,
)
from bs_db_migration.domain_dictionary import DomainDictionary

# configuration = Configuration("config/config.yaml")
# print(configuration.get("db_connection"))


class MS2Postgres:
    TARGET_DEFAULT_COLUMNS = "created_at, updated_at, domain_id, creator_id, updater_id"

    def __init__(self, config_file_path=None, config_data=None):
        self.mssql = None
        try:
            # get the configuration
            self.configuration = Configuration(config_file_path, config_data)

            # try to connect a mssql database
            connection_info = self.configuration.db_info(ConfigDBType.MSSQL)
            (host, port, id, pw, db) = self.configuration.get_connection_info(
                connection_info
            )
            self.mssql = ms.connect(
                server=f"{host}:{port}",
                user=id,
                password=pw,
                database=db,
                charset="utf8",
            )

            # try to connect a postgres database
            connection_info = self.configuration.db_info(ConfigDBType.POSTGRES)
            (host, port, id, pw, db) = self.configuration.get_connection_info(
                connection_info
            )
            self.postgres = pg2.connect(
                user=id, password=pw, host=host, port=port, database=db
            )

            # TODO:
            migration_info = self.configuration.migration_info()
            self.migraiton_table_list: list = []
            self.migration_info_available = migration_info.get("use", False)
            if self.migration_info_available:
                migration_connection_info = migration_info["connection"]
                (host, port, id, pw, db) = self.configuration.get_connection_info(
                    migration_connection_info
                )
                self.mginfo = pg2.connect(
                    user=id,
                    password=pw,
                    host=host,
                    port=port,
                    database=db,
                )

                with self.mginfo.cursor() as cursor:
                    cursor.execute(
                        f"SELECT id, type, source_table_name, target_table_name FROM migration_info;"
                    )
                    self.migraiton_table_list = cursor.fetchall()

        except Exception as ex:
            log_error(f"Can't connect databases: {ex}")
            raise ex

    def close(self):
        self.mssql.close()
        self.postgres.close()
        self.mginfo.close()

    def get_source_table_scheme(self, table_name: str) -> list:
        cursor = self.mssql.cursor(as_dict=True)
        cursor.execute(f"exec sp_columns {table_name};")
        schema_info = cursor.fetchall()
        cursor.close()
        return schema_info

    @print_execution_time
    def create_table_without_migration_info(self, table_name: str) -> None:
        # get table info. of MSSQL
        cursor = self.mssql.cursor(as_dict=True)
        cursor.execute(f"exec sp_columns {table_name};")
        schema_info = cursor.fetchall()
        cursor.close()

        # create a new table
        sql_create_table = f"CREATE TABLE {table_name} "
        sql_create_table += "( "
        # TODO: add 'UNIQUE'
        for scheme in schema_info:
            sql_create_table += f'{scheme["COLUMN_NAME"]} {MS2PostgresTypeMapping.convert_type(scheme)} {MS2PostgresTypeMapping.convert_nuallable(scheme)}, '
        sql_create_table = sql_create_table[:-2]
        sql_create_table += " );"

        with self.postgres.cursor() as cursor:
            cursor.execute(sql_create_table)
            cursor.close()
            self.postgres.commit()

    @print_execution_time
    def migrate_table_without_migration_info(self, table_name: str) -> None:
        # get records and scheme infor from a source(MSSQL)
        start_time = time.time()
        cursor = self.mssql.cursor(as_dict=True)
        cursor.execute(f"exec sp_columns {table_name};")
        schema_info = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {table_name};")
        record_list = cursor.fetchall()
        cursor.close()
        end_time = time.time()
        print(f"execution time (MSSQL): {end_time - start_time} (sec)")

        # generate insert sql
        sql_insert_multiple_values = ""
        """
        create the sql string with the following syntax

        INSERT INTO table_name (column_list)
        VALUES
            (value_list_1),
            (value_list_2),
            ...
            (value_list_n)
        """
        start_time = time.time()
        sql_insert_multiple_values += f"INSERT INTO {table_name} ("
        for scheme in schema_info:
            sql_insert_multiple_values += f'{scheme["COLUMN_NAME"]}, '
        sql_insert_multiple_values = sql_insert_multiple_values[:-2]
        sql_insert_multiple_values += ") VALUES %s;"

        values_list = list()
        for records in record_list:
            record_list = list()
            for record in records:
                record_list.append(records[record])
            values_list.append(tuple(record_list))
        end_time = time.time()
        print(f"execution time (SQL Ready): {end_time - start_time} (sec)")

        # insert records with the generated sql
        start_time = time.time()
        with self.postgres.cursor() as cursor:
            extras.execute_values(cursor, sql_insert_multiple_values, values_list)
            cursor.close()
            self.postgres.commit()
        end_time = time.time()
        print(f"execution time (POSTGRES): {end_time - start_time} (sec)")

    def get_migration_items(self) -> list:
        """
        return migration_table_list. this list is got from query 'SELECT id, source_table_name, target_table_name FROM migration_info;' in migration_info database

        so, summary the meaning of index
        0: id
        1: type
        2: source_table_name
        3: target_table_name

        """
        return self.migraiton_table_list

    def get_source_table_count(self, table_name: str, domain_name: str) -> int:
        with self.mssql.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM {table_name} WHERE DATAAREAID = '{domain_name}';"
            )
            count = cursor.fetchone()[0]
            cursor.close()
            return count

    def get_target_table_count(self, table_name: str, domain_name: str) -> int:
        target_domain_id = self.get_target_domain_id(domain_name)
        with self.postgres.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(*) FROM {table_name} WHERE domain_id = '{target_domain_id}';"
            )
            count = cursor.fetchone()[0]
            cursor.close()
            return count

    def get_source_table_data(
        self, table_name: str, columns: str, source_domain_name: str
    ) -> int:
        with self.mssql.cursor() as cursor:
            cursor.execute(
                f"SELECT {columns} FROM {table_name} WHERE DATAAREAID = '{source_domain_name}';"
            )
            soure_data = cursor.fetchall()
            cursor.close()
            return soure_data

    def get_target_table_data(
        self, table_name: str, columns: str, source_domain_name: str
    ) -> int:
        target_domain_id = self.get_target_domain_id(
            DomainDictionary.get(source_domain_name)
        )
        with self.postgres.cursor() as cursor:
            cursor.execute(
                f"SELECT {columns} FROM {table_name} WHERE domain_id = '{target_domain_id}';"
            )
            target_data = cursor.fetchall()
            cursor.close()
            return target_data

    def get_migration_data(self, migration_type: str) -> tuple:
        for [
            id,
            type,
            source_table_name,
            target_table_name,
        ] in self.migraiton_table_list:
            if migration_type == type:
                with self.mginfo.cursor() as cursor:
                    cursor.execute(
                        f"SELECT source_column_name, source_column_type, source_size, target_column_name, target_column_type, target_size, target_null_yn FROM migration_info_detail mid where mid.migration_info_id = '{id}';"
                    )
                    column_info = cursor.fetchall()
                    cursor.close()
                    # TODO: check if target table(postgres) name should be lower string or not
                    return (source_table_name, target_table_name.lower(), column_info)

        return None

    def check_target_table_exist(self, target_table_name: str) -> bool:
        sql_str = f"SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = '{target_table_name}');"
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_str)
            result = cursor.fetchone()
            cursor.close()

            # the result is like (True,) or (False,), so we need to return the first element
            return result[0]

    def delete_target_table(self, target_table_name: str) -> None:
        sql_str = f"DROP TABLE {target_table_name};"
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_str)
            cursor.close()

        self.postgres.commit()

    def create_target_table_with_migration_info(
        self, migration_type: str, table_recreate: bool = False
    ) -> None:
        # get table names and column info. from migration info.
        (_, target_table_name, column_info_list) = self.get_migration_data(
            migration_type
        )

        # check if the target table already exists and if it should be recreated
        check_result = self.check_target_table_exist(target_table_name)
        if check_result and table_recreate:
            log_info(f"table {target_table_name} will be deleted and recreated")
            self.delete_target_table(target_table_name)
        elif check_result and not table_recreate:
            log_info(f"table {target_table_name} already exists")
            return

        """
        create the sql string with the following syntax

        CREATE TABLE target_table_name (column #1, column #2, ... , column #n)
        """

        # create a new table with the column info.
        sql_create_table = f"CREATE TABLE {target_table_name} "
        sql_create_table += "( "

        for column_info in column_info_list:
            if column_info[3] in ["ID", "id"]:
                sql_create_table += (
                    f"{column_info[3]} uuid DEFAULT uuid_generate_v4(), "
                )
            else:
                sql_create_table += f"{column_info[3]} {PostgresTypeMapping.convert_type(column_info[4], column_info[5])} {PostgresTypeMapping.convert_nuallable(column_info[6])}, "
        sql_create_table = sql_create_table[:-2]
        sql_create_table += " );"
        log_debug(sql_create_table)

        # apply the sql
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_create_table)
            cursor.close()
            self.postgres.commit()

    def clear_target_table(self, migration_type: str) -> None:
        # get table names and column info. from migration info.
        (_, target_table_name, column_info_list) = self.get_migration_data(
            migration_type
        )

        """
        create the sql string with the following syntax

        TRUNCATE {table_name}
        """

        # create a new table with the column info.
        sql_create_table = f"TRUNCATE {target_table_name};"

        # apply the sql
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_create_table)
            cursor.close()
        self.postgres.commit()

    def convert_record_type(self, data_type: str, data_value: any) -> any:
        """
        TODO: generate the converting rule based on migration from MSSQL DB column type to POSTGRES DB column type

        """
        if data_type == "VARCHAR":
            return str(data_value)
        elif data_type == "BOOLEAN":
            return False if data_value in [0, None, "0"] else True
        else:
            return data_value

    def get_target_domain_id(self, domain_name: str) -> str:
        sql_str = f"SELECT id FROM domains WHERE name = '{domain_name}';"
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_str)
            result = cursor.fetchone()
            cursor.close()

            return result[0]

    def get_target_admin_user_id(self):
        admin_email = "admin@hatiolab.com"

        sql_str = f"SELECT id FROM users WHERE email = '{admin_email}';"
        with self.postgres.cursor() as cursor:
            cursor.execute(sql_str)
            result = cursor.fetchone()
            cursor.close()

            return result[0]

    def create_target_extra_values(self, domain_id: str, user_id: str) -> list:
        """
        EXTRA COLUMNS
        created_at, updated_at, domain_id, creator_id, updater_id

        """
        return [
            "NOW()",
            "NOW()",
            domain_id,
            user_id,
            user_id,
        ]

    def get_column_list_string(self, column_info_list: list) -> list:
        # get column list from migration table info.
        """
        column_info -> [source_column_name, source_column_type, source_size, target_column_name, target_column_type, target_size, target_null_yn]
        """
        source_column_list_string = ""
        target_column_list_string = ""
        target_column_type_list = list()
        for column_info in column_info_list:
            source_column_list_string += (
                column_info[0] + ", " if column_info[0] != "?" else ""
            )

            if column_info[3] == "ID" or column_info[3] == "id":
                pass
            else:
                target_column_list_string += (
                    ""
                    if column_info[3] == "ID" or column_info[3] == "id"
                    else column_info[3] + ", "
                )
                target_column_type_list.append(column_info[4])

        # finalize the column list string
        source_column_list_string = source_column_list_string[:-2]
        target_column_list_string += MS2Postgres.TARGET_DEFAULT_COLUMNS
        return (
            source_column_list_string,
            target_column_list_string,
            target_column_type_list,
        )

    @print_execution_time
    def migrate_all_data_once(
        self, migration_type: str, source_domain_name: str = "seg"
    ) -> None:
        # get table names and column info. from migration info.
        (
            source_table_name,
            target_table_name,
            column_info_list,
        ) = self.get_migration_data(migration_type)

        # get column list from migration table info.
        (
            source_column_list_string,
            target_column_list_string,
            target_column_type_list,
        ) = self.get_column_list_string(column_info_list)

        # get records from a source(MSSQL)
        start_time = time.time()
        cursor = self.mssql.cursor(as_dict=True)
        cursor.execute(
            f"SELECT {source_column_list_string} FROM {source_table_name} WHERE DATAAREAID = '{source_domain_name}';"
        )
        source_record_list = cursor.fetchall()
        cursor.close()
        end_time = time.time()
        print(f"execution time (READ FROM MSSQL): {end_time - start_time} (sec)")

        # generate insert sql
        sql_insert_multiple_values = ""
        """
        create the sql string with the following syntax

        INSERT INTO source_table_name (column_list)
        VALUES
            (value_list_1),
            (value_list_2),
            ...
            (value_list_n)
        """
        start_time = time.time()
        sql_insert_multiple_values += (
            f"INSERT INTO {target_table_name} ({target_column_list_string}"
        )
        sql_insert_multiple_values += ") VALUES %s;"

        # fetch user id and domain id
        domain_id = self.get_target_domain_id(DomainDictionary.get(source_domain_name))
        user_id = self.get_target_admin_user_id()
        if not domain_id or not user_id:
            raise Exception("domain or user could be not found in the target DB.")

        values_list = list()
        for records in source_record_list:
            record_list = list()
            for idx, record in enumerate(records):
                # TODO: check if data type is correct here
                records[record] = self.convert_record_type(
                    target_column_type_list[idx], records[record]
                )
                record_list.append(records[record])
            # append extra column values
            record_list += self.create_target_extra_values(domain_id, user_id)
            values_list.append(tuple(record_list))

        end_time = time.time()
        print(f"execution time (SQL Ready): {end_time - start_time} (sec)")

        # insert records with the generated sql
        start_time = time.time()
        with self.postgres.cursor() as cursor:
            extras.execute_values(cursor, sql_insert_multiple_values, values_list)
            cursor.close()
            self.postgres.commit()
        end_time = time.time()
        print(f"execution time (POSTGRES): {end_time - start_time} (sec)")

    @print_execution_time
    def migrate_all_data(
        self,
        migration_type: str,
        source_order_by_column: str,
        read_size: int = 100000,
        source_domain_name: str = "seg",
    ) -> None:
        # get table names and column info. from migration info.
        (
            source_table_name,
            target_table_name,
            column_info_list,
        ) = self.get_migration_data(migration_type)

        # get column list from migration table info.
        (
            source_column_list_string,
            target_column_list_string,
            target_column_type_list,
        ) = self.get_column_list_string(column_info_list)

        # get records from a source(MSSQL)
        total_record_count = self.get_source_table_count(
            source_table_name, source_domain_name
        )

        # fetch user id and domain id
        domain_id = self.get_target_domain_id(DomainDictionary.get(source_domain_name))
        user_id = self.get_target_admin_user_id()
        if not domain_id or not user_id:
            raise Exception("domain or user could be not found in the target DB.")

        for i in range(0, total_record_count, read_size):
            start_time = time.time()
            cursor = self.mssql.cursor(as_dict=True)

            source_sql = f"SELECT {source_column_list_string} FROM {source_table_name} WHERE DATAAREAID = '{source_domain_name}' ORDER BY {source_order_by_column} OFFSET {i} ROWS FETCH NEXT {read_size} ROWS ONLY;"
            print(source_sql)
            cursor.execute(source_sql)
            source_record_list = cursor.fetchall()
            cursor.close()

            # generate insert sql
            sql_insert_multiple_values = ""
            """
            create the sql string with the following syntax

            INSERT INTO source_table_name (column_list)
            VALUES
                (value_list_1),
                (value_list_2),
                ...
                (value_list_n)
            """
            sql_insert_multiple_values += (
                f"INSERT INTO {target_table_name} ({target_column_list_string}"
            )
            sql_insert_multiple_values += ") VALUES %s;"

            values_list = list()
            for records in source_record_list:
                record_list = list()
                for idx, record in enumerate(records):
                    # TODO: check if data type is correct here
                    records[record] = self.convert_record_type(
                        target_column_type_list[idx], records[record]
                    )

                    record_list.append(records[record])
                record_list += self.create_target_extra_values(domain_id, user_id)
                values_list.append(tuple(record_list))

            # insert records with the generated sql
            with self.postgres.cursor() as cursor:
                extras.execute_values(cursor, sql_insert_multiple_values, values_list)
                cursor.close()
                self.postgres.commit()
            end_time = time.time()
            print(f"execution time ({i}): {end_time - start_time} (sec)")

    def check_table_data_count(
        self, mssql_table: str, postgres_table: str, source_domain_name: str
    ) -> bool:
        mssql_count = self.get_source_table_count(mssql_table, source_domain_name)
        postgres_count = self.get_target_table_count(
            postgres_table.lower(), DomainDictionary.get(source_domain_name)
        )
        if mssql_count == postgres_count:
            return True
        else:
            return False

    def check_table_data_all(
        self, migration_type: str, source_domain_name: str
    ) -> bool:
        # get table names and column info. from migration info.
        (
            source_table_name,
            target_table_name,
            column_info_list,
        ) = self.get_migration_data(migration_type)

        # get column list from migration table info.
        (
            source_column_list_string,
            target_column_list_string,
            target_column_type_list,
        ) = self.get_column_list_string(column_info_list)

        source_data = self.get_source_table_data(
            source_table_name, source_column_list_string, source_domain_name
        )
        target_data = self.get_target_table_data(
            target_table_name, target_column_list_string, source_domain_name
        )

        # TODO: compare data with the same order
        print(source_data)

        return True
