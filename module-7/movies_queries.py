import os
import mysql.connector
from mysql.connector import errorcode

# Load environment variables
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "127.0.0.1")
database = os.getenv("DB_NAME", "movies")

# Database connection config using environment variables
config = {
    "user": user,
    "password": password,
    "host": host,
    "database": database,
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Query 1: Select all fields from the studio table
    print("-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    for studio in studios:
        print(f"Studio ID: {studio[0]}\nStudio Name: {studio[1]}\n")
    print()  # Add an extra newline for better formatting

    # Query 2: Select all fields from the genre table
    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    for genre in genres:
        print(f"Genre ID: {genre[0]}\nGenre Name: {genre[1]}\n")
    print()

    # Query 3: Select movies with runtime less than 2 hours (120 minutes)
    print("-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    short_films = cursor.fetchall()
    for film in short_films:
        print(f"Film Name: {film[0]}\nRuntime: {film[1]}\n")
    print()

    # Query 4: Select films and directors, grouped by director
    print("-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    directors = cursor.fetchall()
    for director in directors:
        print(f"Film Name: {director[0]}\nDirector: {director[1]}\n")
    print()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cursor.close()
    db.close()
