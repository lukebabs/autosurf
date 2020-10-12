import time, random, getpass, platform
import cx_Oracle
import pyodbc

def main():
    try:
        thread_timer = int(input("Enter simulation time in seconds e.g. 600 = 6 monutes > "))
    except:
        print ('Value is not an integer')
        return
    
    '''Using system timer to trick the process to only run for specified time'''
    current_time = time.time()
    elapsed_time = current_time+thread_timer #elapsed_time will be greater than or equal to current time to allow the processs to run at least once

    while int(time.time()) <= elapsed_time:
        dump_tables()

def dbConnect_orcl():
    pltOS = platform.system() #This helps identify the base OS - Darwin (Apple) or Windows
    if pltOS == 'Darwin':
        #Need cx_Oracle installed - https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
        #Store in directory to be referenced below
        cx_Oracle.init_oracle_client(lib_dir="./drivers/mac/oracle/instantclient_19_3-2")

    elif pltOS == 'Windows':
        cx_Oracle.init_oracle_client(lib_dir="./drivers/windows/oracle/instantclient_19_3-2")
    database = input("Enter DB instance e.g. '192.168.0.204/orcl' > ")
    username = input("Enter username for DB e.g. 'superveda_db' > ")
    password = getpass.getpass()
    try:
        connection = cx_Oracle.connect(username, password, database)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print (e)

def dbConnect_mssql():
    driver="{ODBC Driver 17 for SQL Server}"
    server = input("Enter MSSQL host name or IP address > ")
    database = input("Enter database name e.g. 'superveda_db' >")
    username = input("Enter DB username > ")
    password = getpass.getpass()
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = conn.cursor()
    return cursor


def get_tables_mssql():
    cursor = dbConnect_mssql()
    cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')
    tables = []
    for row in cursor:
        tables.append(row[2]) #Extract only tables from response and append tables list
    return tables, cursor


def get_tables_oracle():
    cursor = dbConnect_orcl()
    cursor.execute("SELECT * FROM tab") #Find all tables in the database
    tables = []
    for values in cursor:
        table_list = values[0]
        tables.append(table_list)
    return tables, cursor


def db_type(dbtype):
    if dbtype == "oracle":
        tables, cursor = get_tables_oracle()
        return tables, cursor
    elif dbtype == "mssql":
        tables, cursor = get_tables_mssql()
        return tables, cursor

def dump_tables(dbtype):
    tables, cursor = db_type(dbtype)
    random.shuffle(tables) #Shuffle the list so that the queries are random
    for items in tables:
        time.sleep(2)
        print (f'\nResponse from {items} table:\n')
        try:
            cursor.execute(f"SELECT * FROM {items}")
            for data in cursor:
                print (data)
        except Exception as v:
            print (v, items)

def menu():
    menu=True
    while menu:
        print("""
        ** Caution: Under development.
        DB Decepticon can be used to generate random queries to a database

        1. Oracle
        2. MSSQL
        3. Exit
        """)

        menu=input("What would you like to do? ")
        if menu=="1":
            print("\n Oracle")
            dump_tables("oracle")
        elif menu=="2":
            print("\n MSSQL")
            dump_tables("mssql")
        elif menu=="3" or "q":
            break
        elif menu == None:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":
    main()