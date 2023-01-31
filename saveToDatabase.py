import json
import mysql.connector
import logging

from parseJSON import LXC_Container

def initialize_MySQL() -> mysql.connector.MySQLConnection:
    """Initialize MySQL with connection details specified in 'connection.json' and create the required tables, dropping them if exist."""
    logging.info("Initializing MySQL with user data in 'connection.json'")
    try:
        with open("connection.json", "r", encoding="utf-8") as f:
            database = mysql.connector.connect(
                **json.loads(f.read())
            )
    except Exception as err:
        logging.exception("Cannot connect to MySQL", exc_info=True)
    else:
        logging.info("MySQL initialized.")
        
    logging.info("Creating table 'containers'")
    cursor = database.cursor()
    cursor.execute("""DROP TABLE IF EXISTS containers""")
    cursor.execute("""DROP TABLE IF EXISTS addresses""")
    
    create_table = """CREATE TABLE containers
    (name VARCHAR(255),
    cpu_usage INT,
    memory_usage INT,
    created_at TIMESTAMP,
    status VARCHAR(255)
    )
    """
    try:
        cursor.execute(create_table)
    except Exception as err:
        logging.exception("Cannot create table 'containers'", exc_info=True)
    else:
        logging.info("Table 'containers' created")
    
    logging.info("Creating table 'addresses'")
    # IP adresy mohou mít 39
    create_addresses = """CREATE TABLE addresses
    (name VARCHAR(255),
    address VARCHAR(39)
    )"""
    try:
        cursor.execute(create_addresses)
    except Exception as err:
        logging.exception("Cannot CREATE table 'adresses'", exc_info=True)
    else:
        logging.info("Table 'addresses' created")
    return database


def save_to_database(database: mysql.connector.MySQLConnection, data: list[LXC_Container]):
    """Take the list of LXC_Containers and write it to tables named 'containers' and 'addresses'."""
    
    logging.info("Writing data to tables")
    
    try:
        cursor = database.cursor()
        
        containers_tuple = [(x.name, x.cpu, x.memory, x.created_at, x.status) for x in data]
        command = "INSERT INTO containers VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(command, containers_tuple)
        
        addresses_tuple = [(container.name, address) for container in data for address in container.addresses]
        command = "INSERT INTO addresses VALUES (%s, %s)"
        cursor.executemany(command, addresses_tuple)
    except Exception as err:
        logging.exception("Cannot write data to tables", exc_info=True)
    
    database.commit()
