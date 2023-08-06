# milho-multi-sqlite3-manager

## Description

The idea is to have an environment with multiple SQLITE3 files, aiming at ease of access and use.
The inspiration for creating this module came from the ease of working with Spark in BigData environments where, generally, everything is integrated, without the need to make several explicit connections in the code.

If you want an integrated environment on your machine, create an environment variable called "MULTISQLITE3MANAGER_FOLDER_PATH" with the directory of your folder. You will need to make sure that all files in this folder are SQLITE3 databases.

When "to_dataframe" is used, the result is a Pandas DataFrame. The query is previously parsed to map all the databases used in the SQL. Then the module create a sqlalchemy connection and attach that databases to the connection. After that, the query is executed and the result is a Pandas DataFrame. 

## Code Samples

```python

from multisqlite3manager import print_databases, print_tables, to_dataframe

print_databases()
print_tables("DB_NAME")

df = to_dataframe("SELECT * FROM db_1.tMisto")
df2 = to_dataframe("SELECT * FROM db_2_copy.tMisto")

```
