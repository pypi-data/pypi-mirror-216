import sqlalchemy
import dataclasses
import sqlglot
import os 
import glob
import pandas
import typing

MULTISQLITE3MANAGER_FOLDER_PATH_KEY = "MULTISQLITE3MANAGER_FOLDER_PATH"
MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT = os.getenv(MULTISQLITE3MANAGER_FOLDER_PATH_KEY)

@dataclasses.dataclass
class _Database:
    """
        A class to represent a database.
        :param db_name: The database name.
        :param filename: The database filename.
    """
    db_name: str
    filename: str

@dataclasses.dataclass
class StorageEnvManager:
    """
        A class to represent a storage environment manager.
        :param databases: A list of _Database objects.
        :param database_folder_path: The path of the folder that stores the database files
    """
    databases: list[_Database]
    database_folder_path: str

def _create_storage_env_manager(database_folder_path: str) -> StorageEnvManager:
    """
        Create a StorageEnvManager object.
        :param database_folder_path: The folder path where the sqlite3 database files are located.
        :return: A StorageEnvManager object.
    """

    if not os.path.isdir(database_folder_path):
        raise NotADirectoryError(f"The folder path {database_folder_path} is not a directory.")

    files = glob.glob(f'{database_folder_path}/*') 

    if len(files) == 0:
        raise FileNotFoundError(f"The folder path {database_folder_path} does not contain any sqlite3 database file.")

    databases = []

    for file in files:
        db_name, _ = os.path.splitext(os.path.basename(file))
        databases.append(_Database(db_name, file))

    return StorageEnvManager(databases, database_folder_path)

def _create_connection_with_attached_databases(databases: typing.List[_Database]) -> sqlalchemy.engine.base.Engine:
    """
        Create a connection with attached databases.
        :param databases: A list of _Database objects.
        :return: A sqlalchemy.engine.base.Engine object.
    """

    from sqlalchemy import text
    
    if len(databases) == 0:
        raise ValueError("The databases list is empty.")

    engine = sqlalchemy.create_engine('sqlite://', echo=False)

    with engine.connect() as conn:
        for db in databases:
            conn.execute(text(f"ATTACH DATABASE '{db.filename}' AS {db.db_name};"))

        return engine

def _get_databases_name_from_sql_stmt(sql: str) -> list[str]:
    """
        Get all databases names from a sql statement.
        :param sql: The sql statement.
        :return: A list of databases names.
    """

    tables = [x for x in sqlglot.parse_one(sql).find_all(sqlglot.exp.Table)]
    parts = [str(x).split('.') for x in tables]
    dbs = [x[0] for x in parts if len(x) > 1]

    return dbs

def _validate_folder_path(folder_path: str):
    """
        Validate the folder path
        :param folder_path: The folder path where the sqlite3 database files are located.
    """
    if folder_path == None and MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT == None:
        return False
    
    return True

def to_dataframe(sql: str, folder_path: str = MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT) -> pandas.DataFrame:
    """
        Execute a sql statement in all sqlite3 database files in the folder_path. Attach all databases in the SQL to the connection and execute the sql statement.
        :param folder_path: A dataframe with the result of the sql statement.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_FOLDER_PATH_KEY}")
    
    stmt_dbs = _get_databases_name_from_sql_stmt(sql)
    env_manager = _create_storage_env_manager(folder_path)
    storage_env_databases = [x.db_name for x in env_manager.databases]

    if len(stmt_dbs) == 0:
        raise ValueError("The sql statement does not contain any database name.")

    for db in stmt_dbs:
        if db not in storage_env_databases:
            raise ValueError(f"The database {db} does not exist in the storage environment.")
        
    databases = [x for x in env_manager.databases if x.db_name in stmt_dbs]

    engine = _create_connection_with_attached_databases(databases)

    with engine.connect() as conn:
        return pandas.read_sql(sql, conn)

def create_connection(databases: typing.List[str], folder_path: str = MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT) -> sqlalchemy.engine.base.Connection:
    """
        Create a connection with attached databases.
        :param databases: A list of databases names.
        :param folder_path: The folder path where the sqlite3 database files are located.
        :return: A sqlalchemy.engine.base.Connection object.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_FOLDER_PATH_KEY}")

    env_manager = _create_storage_env_manager(folder_path)
    storage_env_databases = [x.db_name for x in env_manager.databases]

    if len(databases) == 0:
        raise ValueError("The databases list is empty.")

    for db in databases:
        if db not in storage_env_databases:
            raise ValueError(f"The database {db} does not exist in the storage environment.")

    dbs = [x for x in env_manager.databases if x.db_name in databases]

    return _create_connection_with_attached_databases(dbs).connect()

def print_databases(folder_path: str = MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT):
    """
        Print all databases in the folder_path.
        :param folder_path: The folder path where the sqlite3 database files are located.
    """

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_FOLDER_PATH_KEY}")

    env_manager = _create_storage_env_manager(folder_path)

    for db in env_manager.databases:
        print('-> ', db.db_name, ' - ', db.filename)

def print_tables(database_name: str, folder_path: str = MULTISQLITE3MANAGER_FOLDER_PATH_DEFAULT):
    """
        Print all tables in the database.
        :param database: The database name.
        :param folder_path: The folder path where the sqlite3 database files are located.
    """
    from sqlalchemy import text

    if not _validate_folder_path(folder_path):
        raise Exception(f"You must provide a folder path or set the environment variable {MULTISQLITE3MANAGER_FOLDER_PATH_KEY}")

    env_manager = _create_storage_env_manager(folder_path)

    if database_name not in [x.db_name for x in env_manager.databases]:
        raise ValueError(f"The database {database_name} does not exist in the storage environment.")

    engine = _create_connection_with_attached_databases([x for x in env_manager.databases if x.db_name == database_name])

    with engine.connect() as conn:
        tables = conn.execute(text(f"SELECT name FROM {database_name}.sqlite_master WHERE type='table';"))
        for table in tables:
            print('-> ', database_name, ' - ', table[0])