import records
import json
import pandas
from secrets import sql_user, sql_passwd


def typeHelper(key, value):
    value_type = type(value)
    if value_type is int:
        return ('INT', value)
    elif value_type is float:
        return ('DECIMAL', value)
    elif value_type is bool:
        return ('BIT', 1 if value is True else 0)
    else:
        if 'id' in key:
            return ('INT', value if value is not None else 'NULL')
        else:
            return ('NVARCHAR(MAX)', value if value is not None else 'NULL')


def getSchema(json_object, no_types=None):
    first_object = list(json_object.items())
    first_pair = first_object.pop(0)
    key = first_pair[0]
    value = first_pair[1]
    column_type, column_val = typeHelper(key, value)
    if no_types is True:
        schema_str = "{}".format(key)
    else:
        schema_str = "{} {}".format(key, column_type)

    for key, val in first_object:
        column_type, column_val = typeHelper(key, val)
        if no_types is True:
            schema_str += ", {}".format(key)
        else:
            schema_str += ", {} {}".format(key, column_type)

    return schema_str


def getValues(json_object):
    first_object = list(json_object.items())
    first_pair = first_object.pop(0)
    key = first_pair[0]
    value = first_pair[1]
    column_type, column_val = typeHelper(key, value)
    if column_type == "NVARCHAR(MAX)" and column_val != "NULL":
        if "'" in column_val:
            value_str = "'{}'".format(column_val.replace("'", "''"))
        else:
            value_str = "'{}'".format(column_val)
    else:
        value_str = "{}".format(column_val)

    for key, val in first_object:
        column_type, column_val = typeHelper(key, val)
        if column_type == 'NVARCHAR(MAX)' and column_val != "NULL":
            if "'" in column_val:
                value_str += ", '{}'".format(column_val.replace("'", "''"))
            else:
                value_str += ", '{}'".format(column_val)
        else:
            value_str += ", {}".format(column_val)

    return value_str


# Log into the MS-SQL Server using a user-specified DSN.  I called mine
# "PSI-SQL-DSN"
if os.name == 'posix':
    server = "AWS-SQL"
    username = sql_user
    password = sql_passwd
    db = records.Database(db_url="mssql://{}:{}@{}".format(username,
                                                           password,
                                                           server))
else:
    server = "PSI-SQL-DSN"
    db = records.Database(db_url="mssql://" + server)

filename = "tsysAssetTypes"


db.query("""
    IF EXISTS (SELECT * FROM sys.tables where name='{}') DROP TABLE {}
""".format(filename, filename))


with open(filename + ".json") as my_json_file:
    d = json.load(my_json_file)

print(getSchema(d[0]) + "\n")
# print(getValues(d[0]))

create_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables where name='{}')
        CREATE TABLE {} ({});
""".format(filename, filename, getSchema(d[0]))

db.query(create_query)

for index, entry in enumerate(d):
    insert_query = """
        INSERT INTO {} ({}) VALUES ({})
    """.format(filename,
               getSchema(entry, no_types=True),
               getValues(entry))
    try:
        db.query(insert_query)
    except Exception as e:
        print("Error entry {} Query: \n{}\n Exception: {}".format(index,
                                                                  insert_query,
                                                                  e))
