import mysql.connector
from parseJSON import LXC_Container

def initialize_MySQL() -> mysql.connector.MySQLConnection:
    """Initialize MySQL and create a database if it does not exist."""
    database = mysql.connector.connect(
        host = "localhost",
        user = "blazniva_ponozka",
        passwd="blazniva_ponozka_2023_6969696969_MoznaVelkyPismena",
        database="lxc_containers"
    )
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
    cursor.execute(create_table)
    
    # IP adresy mohou mít 39
    create_addresses = """CREATE TABLE addresses
    (name VARCHAR(255),
    address VARCHAR(39)
    )"""
    
    cursor.execute(create_addresses)
    
    return database


def save_to_database(database: mysql.connector.MySQLConnection, data: list[LXC_Container]):
    cursor = database.cursor()
    
    containers_tuple = [(x.name, x.cpu, x.memory, x.created_at, x.status) for x in data]
    command = "INSERT INTO containers VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(command, containers_tuple)
    
    addresses_tuple = [(container.name, address) for container in data for address in container.addresses]
    command = "INSERT INTO addresses VALUES (%s, %s)"
    cursor.executemany(command, addresses_tuple)
    
    database.commit()
