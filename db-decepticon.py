import time, random, getpass, platform, getopt, sys
import cx_Oracle
import pyodbc
import mysql.connector as connector
from sqlalchemy import create_engine

class Database(): #This class is not yet active. It will be used when multiple users are used to simulate traffic
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

def main():
    dbtype = ''
    try:
        opts, arg = getopt.getopt(sys.argv[1:],"t:")
        for opt, arg in opts:
            if opt == '-t':
                dbtype = str(arg)
                return dbtype  #returns the variables to be used as inputs in other functions
    except getopt.GetoptError as e:
        print (e, 'python db_decepticon -t oracle')
        sys.exit(2)

def initate_timer():
    try:
        thread_timer = int(input("Enter simulation time in seconds e.g. 600 = 10 minutes > "))
    except:
        print ('Value is not an integer')
        return
    
    '''Using system timer to trick the process to only run for specified time'''
    current_time = time.time()
    elapsed_time = current_time+thread_timer #elapsed_time will be greater than or equal to current time to allow the processs to run at least once

    while int(time.time()) <= elapsed_time:
        dump_tables()


def dbConnect_mysql():
    try:
        config = {
            "host":server,
            "user":username,
            "password":password,
            "database":database
        }
        cursor = connector.connect(**config)
        return cursor
    except Exception as e:
        print (e)
   
def dbConnect_orcl():
    # cx_Oracle.init_oracle_client(lib_dir="./drivers/mac/oracle/instantclient_19_3-2")
    try:
        connection = cx_Oracle.connect(username, password, database)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print (e)

def dbConnect_mssql():
    try:
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
        cursor = conn.cursor()
        return cursor
    except Exception as e:
        print (e)


def get_tables_mssql():
    cursor = dbConnect_mssql()
    cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')
    tables = []
    for row in cursor:
        tables.append(row[2]) #Extract only tables from response and append tables list
    return tables, cursor


def get_tables_oracle():
    # cx_Oracle.init_oracle_client(lib_dir="./drivers/mac/oracle/instantclient_19_3-2")
    print (driver, server, database, username, password)
    connection = cx_Oracle.connect()
    cursor = connection.cursor()
    cursor = dbConnect_orcl()
    cursor.execute("SELECT * FROM tab") #Find all tables in the database
    tables = []
    for values in cursor:
        table_list = values[0]
        tables.append(table_list)
    return tables, cursor

def get_tables_mysql():
    cn = dbConnect_mysql()
    cursor = cn.cursor()
    cursor.execute('SHOW TABLES;')
    tables = []
    for row in cursor:
        tables.append(row[0]) #Extract only tables from response and append tables list
    return tables, cursor


def get_tables():
    if dbtype == "oracle":
        tables, cursor = get_tables_oracle()
        return tables, cursor
    elif dbtype == "mssql":
        tables, cursor = get_tables_mssql()
        return tables, cursor
    elif dbtype == "mysql":
        tables, cursor = get_tables_mysql()
        return tables, cursor

def dump_tables():
    tables, cursor = get_tables()
    random.shuffle(tables) #Shuffle the list so that the queries are random
    for table in tables:
        time.sleep(2)   #Introduce 2 second delay
        print (f'\nResponse from {table} table:\n')

        if dbtype == "mysql":       #This is required because mysql likes the connection to be explicitly reinitiated
            try:
                cn = dbConnect_mysql()
                cursor = cn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                for data in cursor:
                    print (data)
            except Exception as v:
                print (v, table)
        else:
            try:
                cursor.execute(f"SELECT * FROM {table}")
                for data in cursor:
                    print (data)
            except Exception as v:
                print (v, table)

def get_credentials():
    database = "no-val-set"
    server = 'no-val-server'
    username = "no-val-set"
    password = "no-val-set"
    
    if dbtype == 'oracle':
        database = input("Enter DB instance e.g. '192.168.0.204/orcl' > ")
        username = input("Enter username for DB e.g. 'superveda_db' > ")
        password = getpass.getpass()
        return database, server, username, password
    elif dbtype == 'mssql' or 'mysql':
        server = input("Enter Server host name or IP address > ")
        database = input("Enter Database name e.g. 'superveda_db' >")
        username = input("Enter DB username > ")
        password = getpass.getpass()
        return database, server, username, password

if __name__ == "__main__":
    dbtype = main()
    driver="{ODBC Driver 17 for SQL Server}" #MSSQL Driver - this requires installation of Windows ODBC driver. See README
    database, server, username, password = get_credentials() #Get DB credentials from the user
    
    #Identify OS and initialize the DB driver for Oracle. Oracle requires installation of client on OS
    pltOS = platform.system() #This helps identify the base OS - Darwin (Apple) or Windows
    if pltOS == 'Darwin':
        #Need cx_Oracle installed - https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
        #Move it into driver directory as listed below
        cx_Oracle.init_oracle_client(lib_dir="./drivers/mac/oracle/instantclient_19_3-2")
    elif pltOS == 'Windows':
        cx_Oracle.init_oracle_client(lib_dir="./drivers/windows/oracle/instantclient_19_3-2")

    initate_timer()