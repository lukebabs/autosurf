import time, random
import cx_Oracle
import pyodbc
#Need cx_Oracle installed - https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
#Store in directory to be referenced below
cx_Oracle.init_oracle_client(lib_dir="./drivers/mac/oracle/instantclient_19_3-2")

def main():
    try:
        n = int(input("Enter number of iterations > "))
    except:
        print ('Value is not an integer')
        return
    i = 0
    while i < n:
        dump_tables()
        i += 1

def dbConnect_orcl():
    connection = cx_Oracle.connect("superveda_db", "secure123", "192.168.0.204/orcl")
    cursor = connection.cursor()
    return cursor

def dbConnect_mssql():

    driver="{ODBC Driver 17 for SQL Server}"
    server = "192.168.0.202"
    database = "superveda_db"
    username = "sa"
    password = "secure123"
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = conn.cursor()
    return cursor

def get_tables_mssql():
    cursor = dbConnect_mssql()
    cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES')
    tables = []
    for row in cursor:
        tables.append(row[2])
    return tables, cursor

def get_tables_oracle():
    cursor = dbConnect_orcl()
    cursor.execute("SELECT * FROM tab") #Find all tables in the database
    tables = []
    for values in cursor:
        table_list = values[0]
        tables.append(table_list)
    return tables, cursor

def dump_tables():
    tables, cursor = get_tables_mssql()
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

if __name__ == "__main__":
    main()
    # get_tables_mssql()
    # dbConnect_mssql()