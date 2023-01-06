# LXC Parser

The interview assignment.

## Usage:

1. Install MySQL.
2. Create a user with a password:
   `CREATE USER 'username' IDENTIFIED BY 'password';`
3. Create a database:
   `CREATE DATABASE 'db_name';`
4. Grant the user all privileges to the database:
   `GRANT ALL ON db_name.* TO 'username';`
5. Write the connection details to `connection.json`.
6. Run `main.py`.
7. You can view the data:
   `SELECT * FROM containers`, `SELECT * FROM addresses`