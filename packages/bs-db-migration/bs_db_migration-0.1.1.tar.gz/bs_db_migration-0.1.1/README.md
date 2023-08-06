# bs_database_migration
ms2postres is a simple database migration service from mssql to postgres. 
- source database: mssql
- target database: postgres

## how to install
python 3.6, 3.7, 3.8, 3.9

```bash
pip install -r requirements.txt
```

## configuration 
refer to config/config-sample.yaml

```yaml
---
# database connection info. for both source and target database
db_connection:
  # mssql connection info. as a source database
  mssql:
    host: abc.def.com
    port: 1433
    id: admin
    pw: ...
    db: test
  # postgres connection info. as a target database
  postgres:
    host: abc.def.com
    port: 5432
    id: admin
    pw: ...
    db: test

# migration info. like table names of both source and target database and the column list of them
migration_info:
  use: false
  connection:
    host: localhost
    port: 5432
    id: postgres
    pw: password
    db: devmanager
  migration_table: migration_info
  migration_detail_table: migration_info_detail
```

## unit test

```bash
cd src
python3 -m unittest discover -s unit_test -p "*_test.py"
```

## API

### create_table_without_migration_info
create a table in the target database(postgres) using the table information of the source database(mssql).

### migrate_table_without_migration_info
copy all records of the myssql table into the postgres table but this api doesn't create a table in the target database(postgres).
So, you should check if the table exists in the target database(postgres).

### get_migration_data(self, migration_type: str) -> tuple:
get migration table list(source table name and target table name) from *migration_info* table  

### create_target_table_with_migration_info(table_name: str, table_recreate: bool = False) -> None:
create a table in target databse(postgres) based on migration information of the table.
if the table already exists and *recreate* is true, it will remove the existing table and create a new table with the same name.


### migrate_all_data_once(table_name: str) -> None:
migrate all records from mssql to postgres based on migration information of the table

### sample codes

```python
try:
    # create the instance of MS2PostgresMigraiton
    migrator = MS2Postgres(config_file_path="config/config.yaml")

    
    # 
    # migrator.migrate_all_data_once("INVENTTABLEMODULE")

    # get all migration info. from migration info database
    print(migrator.get_migration_data("INVENTTABLEMODULE"))

    # delete all records in the specified table
    migrator.clear_target_table("DIMENSION")

    # migrate all recoreds at once
    migrator.migrate_all_data_once("INVENTTABLEMODULE")

    # migrate records sequentially in increments of 100000. 
    migrator.migrate_all_data("INVENTTABLEMODULE", "ITEMID", 100000)

    migrator.close()
except Exception as ex:
    print("Exception: ", ex)
```
- If you use *migrate_all_data_once*, this is the fastest way to get things done but memory consumption is too high in case of a large of memory
- Use *migrate_all_data* if you need to migrate a large number of records


### Work History

#### Record count
```bash
TKR_INVENTTABLEREQUESTUSE      : 72311
DIMENSIONS                     : 42330
CON_ORGANIZATION               : 5975
BANKACCOUNTTABLE               : 208
TKR_MAKERTABLE                 : 1420
CUSTTABLE                      : 12514
CUSTTABLEGLOBALUSE             : 12204
VENDTABLE                      : 6275
VENDTABLEGLOBALUSE             : 6099
VENDTABLEGLOBAL                : 5183
INVENTTABLE                    : 163440
INVENTTABLEMODULE              : 867246
TKR_STRONGMAKERTABLE           : 33144
PAYMTERM                       : 342
BANKGROUP                      : 665
CASHDISC                       : 190
VENDGROUP                      : 55
DLVTERM                        : 108
DLVMODE                        : 71
CUSTGROUP                      : 52
ADDRESSZIPCODE                 : 289783
ADDRESSCOUNTRYREGION           : 102
TKR_INSURANCERATES             : 54
TKR_TRADETYPETABLE             : 67
TKR_COUNTRYOFORIGINTABLE       : 306
TKR_CRCTABLE                   : 67
TKR_PLCMASTERTABLE             : 36
TKR_AGINGTABLE                 : 44
TKR_GRADETABLE                 : 72
VENDPAYMMODETABLE              : 141
TKR_PURCHASEQUOORIGINTABLE     : 44
PURCHPOOL                      : 68
RETURNACTIONDEFAULTS           : 88
TKR_OFFERTABLE                 : 17
TKR_SALESTYPETABLE             : 93
INVENTTABLEGLOBAL              : 104988
TKR_RESERVMETHODTABLE          : 70
TKR_PROFITCENTERWHTABLE        : 359
TKR_CUSTINVENTDISCTABLE        : 793
TKR_EXPORTTYPEMASTER           : 30
TKR_EXPORTFORWARDMASTER        : 1550
TKR_EXPORTIMPORTACCOUNTMASTER  : 6
PRICEDISCGROUP                 : 28
TKR_CUSTLEVELTABLE             : 30
TKR_QTYCATEGORYTABLE           : 20
SALESORIGIN                    : 63
TKR_DANGERTABLE                : 24
TKR_DELIVERYPAYABLE            : 33
TKR_TRANSFERTYPETABLE          : 33
TKR_MOVEMENTTYPETABLE          : 126
TKR_INVENTBYSALES              : 20
TKR_HSMASTERTABLE              : 3926
TKR_OFFERTYPETABLE             : 12
TKR_CUSTLEVELCALCTABLE         : 77
TKR_CUSTLEVELCALCTABLE         : 77
TKR_KR_VAT_CANCELCODE          : 16
ESG_KR_VATCATGTABLE            : 67
ESG_KR_CREDITCARD              : 774
ESG_KR_TAXOFFICE               : 37
TKR_STRONGMAKERTABLE           : 33144
COMPANYINFO                    : 12
VENDTABLEGLOBAL                : 5183
CUSTTABLEGLOBAL                : 11641
```


#### Elapsed time


##### DIMENSION
```bash
execution time (READ FROM MSSQL): 0.9296822547912598 (sec)
execution time (SQL Ready): 0.3744699954986572 (sec)
execution time (POSTGRES): 8.553436994552612 (sec)
execution time[migrate_all_data_once]: 9.921609878540039 (sec)
```

##### INVENTTABLEMODULE
```bash
# one time read-write
execution time (READ FROM MSSQL): 16.312162160873413 (sec)
execution time (SQL Ready): 4.253669738769531 (sec)
execution time (POSTGRES): 133.28275394439697 (sec)
execution time[migrate_all_data_once]: 154.41863203048706 (sec)

# read-write every 100000 record 
...
execution time (600000): 18.075716733932495 (sec)
execution time (700000): 19.273962020874023 (sec)
execution time (800000): 12.845544815063477 (sec)
execution time[migrate_all_data]: 169.82762694358826 (sec)

# read-write every 10000 record 
...
execution time (840000): 2.7003259658813477 (sec)
execution time (850000): 2.5725209712982178 (sec)
execution time (860000): 2.1922101974487305 (sec)
execution time[migrate_all_data]: 212.86850786209106 (sec)

```

##### AGECODE
```bash
execution time (READ FROM MSSQL): 0.00947713851928711 (sec)
execution time (SQL Ready): 0.00020503997802734375 (sec)
execution time (POSTGRES): 0.02384781837463379 (sec)
execution time[migrate_all_data_once]: 0.04177093505859375 (sec)
```
