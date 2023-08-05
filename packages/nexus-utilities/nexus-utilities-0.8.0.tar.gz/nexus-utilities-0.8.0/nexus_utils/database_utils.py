"""Database-related utilities"""
#%%
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
# from . import config_reader as cr
# from . import password as pw
# from flat_file_loader.src.utils import config_reader as cr
# import config_utils as cr
# from flat_file_loader.src.utils import password as pw
from nexus_utils.package_utils import extract_from_error
import re
import traceback

# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace

#%%
def build_engine_from_env(env_file_path=None):
    """Accept a path to an .env file and build a SQL Alchemy engine object"""

    if env_file_path is not None:
        if isinstance(env_file_path, str):
            env_file_path = env_file_path
        elif isinstance(env_file_path, Path):
            env_file_path = str(env_file_path)
        else:
            print(f'env_file_path must be a string or a Path object.  Type is: {type(env_file_path)}')
            return None
        
        if not os.path.isfile(env_file_path):
            print(f"The specified .env file '{env_file_path}' does not exist.")
            return None
    
        env_vars = {}
        
        try:
            with open(env_file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key] = value
        except Exception as e:
            print(f'Error parsing .env file: {e}')
            return None
    else:
        env_vars = os.environ

    NEXUS_TARGET_DB_CONN_TYPE = env_vars.get('NEXUS_TARGET_DB_CONN_TYPE')
    NEXUS_TARGET_DB_SERVER = env_vars.get('NEXUS_TARGET_DB_SERVER')
    NEXUS_TARGET_DB_PORT = env_vars.get('NEXUS_TARGET_DB_PORT')
    NEXUS_TARGET_DB_DATABASE = env_vars.get('NEXUS_TARGET_DB_DATABASE')
    NEXUS_TARGET_DB_USERNAME = env_vars.get('NEXUS_TARGET_DB_USERNAME')
    NEXUS_TARGET_DB_PASSWORD = env_vars.get('NEXUS_TARGET_DB_PASSWORD')

    engine = build_engine(
        connect_type=NEXUS_TARGET_DB_CONN_TYPE, 
        server_address=NEXUS_TARGET_DB_SERVER, 
        server_port=NEXUS_TARGET_DB_PORT,
        database_name=NEXUS_TARGET_DB_DATABASE,
        user_name=NEXUS_TARGET_DB_USERNAME,
        password=NEXUS_TARGET_DB_PASSWORD
        )
    
    test_result = check_engine_read(engine)

    if test_result != 'Success':
        print(f'Engine read test failed: {test_result}')
        return None
    else:
        return engine

# def build_engine(config_path, config_entry, password_method="keyring"):
def build_engine(connect_type, server_address, server_port, database_name, user_name, password):#, schema=None):
    """Build SQL Alchemy Engine based on input parameters"""
    
    conn_string = f'{connect_type}://{user_name}:{password}@{server_address}:{server_port}/{database_name}'
    # if schema is not None:
        # conn_string += f'?schema={schema}'

    engine = create_engine(conn_string)

    # return engine, schema
    return engine

def check_engine_read(engine, schema=None, table_name=None):
    """Check if the engine object can connect to the specified database and select from it"""
    query_string = 'SELECT 1'
    if schema and table_name:
        query_string = f'SELECT COUNT(*) FROM {schema}.{table_name}'

    if engine is not None:
        try:
            with engine.connect().execution_options(isolation_level='AUTOCOMMIT') as conn:
                result = conn.execute(text(query_string))
            if bool(result.fetchall()):
                return 'Success'
        except OperationalError:
            full_error_message = traceback.format_exc()
            error_message = extract_from_error(full_error_message, 'sqlalchemy.exc')
            if error_message:
                return error_message
            else:
                return full_error_message
    else:
        return 'engine is "None"'

def check_engine_write_delete(engine, schema=None):
    """Check if the engine object can connect to the specified database and create, insert into and delete objects.  Returns 'Success' or the short-form error generated"""
    schema_string = ''
    if schema:
        schema_string = f'{schema}.'
    try:
        with engine.connect().execution_options(isolation_level='AUTOCOMMIT') as conn:
            
            create_table_statement = text(f"CREATE TABLE {schema_string}nexus_access_test (id INT)")
            conn.execute(create_table_statement)

            insert_statement = text(f"INSERT INTO {schema_string}nexus_access_test (id) VALUES (1)")
            conn.execute(insert_statement)

            update_statement = text(f"UPDATE {schema_string}nexus_access_test SET id = 2 WHERE id = 1")
            conn.execute(update_statement)

            select_statement = text(f"SELECT * FROM {schema_string}nexus_access_test")
            result = conn.execute(select_statement)
            records = result.fetchall()

            delete_statement = text(f"DELETE FROM {schema_string}nexus_access_test")
            conn.execute(delete_statement)

            drop_table_statement = text(f"DROP TABLE {schema_string}nexus_access_test")
            conn.execute(drop_table_statement)
            return 'Success'
    except OperationalError as e:
        full_error_message = traceback.format_exc()
        error_message = extract_from_error(full_error_message, 'sqlalchemy.exc')
        if error_message:
            return error_message
        else:
            return full_error_message

def clean_sql_statement(sql_statement):
    """Clean SQL strings to remove comments and separate statements into a list"""
    #%%

    # Remove single-line comments
    sql_statement = re.sub('--(.*?)\n', '', sql_statement)
    sql_statement = re.sub('--(.*?)$', '', sql_statement)

    # Remove multi-line comments
    sql_statement = re.sub(r'/\*(.*?)\*/', '', sql_statement, flags = re.DOTALL)

    # Remove excess line breaks
    while '\n\n' in sql_statement:
        sql_statement = re.sub('\n\n', '\n', sql_statement, flags = re.DOTALL)

    sql_statement = re.sub('^\n', '', sql_statement, flags = re.DOTALL)
    sql_statement = re.sub('\n$', '', sql_statement, flags = re.DOTALL)
    #print(sql_statement)

    sql_statements = sql_statement.split(';')

    sql_statements = [statement.strip() for statement in sql_statements]

    # Remove blank statements
    if "" in sql_statements:
        sql_statements.remove("")
    #print(len(sql_statements))

    # Add ';' to the end of each statement
    sql_statements_output = []
    for statement in sql_statements:
        statement_output = re.sub('^\n', '', statement)
        statement_output = re.sub('\n^', '', statement_output)
        sql_statements_output.append(statement_output + ';')

    return sql_statements_output

#%%
