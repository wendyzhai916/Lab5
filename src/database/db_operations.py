import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'lab05',
}

def create_database(cursor, db_name):
    """
    Creates a database if it does not already exist.
    """
    try:
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_table(cursor):
    """
    Creates a table for storing oil well data.
    """
    table_definition = (
        "CREATE TABLE `wells` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `api_number` varchar(255) NOT NULL,"
        "  `well_name` varchar(255) NOT NULL,"
        "  `longitude` decimal(10, 8) NOT NULL,"
        "  `latitude` decimal(11, 8) NOT NULL,"
        "  `address` varchar(255),"
        "  `stimulation_data` text,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")
    try:
        cursor.execute(table_definition)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table already exists.")
        else:
            print(err.msg)

def insert_well_data(cursor, data):
    """
    Inserts data into the `wells` table.
    """
    add_well = ("INSERT INTO wells "
                "(api_number, well_name, longitude, latitude, address, stimulation_data) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(add_well, data)

def connect_to_database(config):
    """
    Connects to the MySQL database and returns the connection and cursor.
    """
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None, None

def main():
    # Connect to the database
    cnx, cursor = connect_to_database(config)
    if cnx is None or cursor is None:
        return
    
    # Create database and table if they don't exist
    try:
        cnx.database = config['database']
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, config['database'])
            cnx.database = config['database']
            create_table(cursor)
        else:
            print(err)
            exit(1)
    
    # Example data insertion
    example_data = ('123456789', 'Well Name', -98.12345678, 29.12345678, '123 Example St, Example City', 'Example stimulation data')
    insert_well_data(cursor, example_data)
    
    # Commit changes and close connection
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
