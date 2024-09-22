import mysql.connector
from mysql.connector import errorcode
import os

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "127.0.0.1")
database = os.getenv("DB_NAME", "movies")

config = {
    "user": user,  # Use the user from environment variable
    "password": password,  # Use the password from environment variable
    "host": host,
    "database": database,
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    print("Database connection successful!")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    db.close()
