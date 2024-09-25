import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database credentials from the environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def show_films(cursor, title):
    # Method to execute an inner join on all tables and display the results
    cursor.execute("""
        SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """)
    films = cursor.fetchall()

    print(f"\n -- {title} --")
    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre: {film[2]}\nStudio Name: {film[3]}\n")

def main():
    try:
        # Connect to the database
        cnx = mysql.connector.connect(user=db_user, password=db_password,
        host=db_host,
        database=db_name)
        cursor = cnx.cursor()

        # Display initial films
        show_films(cursor, "DISPLAYING FILMS")

        # Insert a new film record
        insert_film_query = """
            INSERT INTO film (film_name, film_director, genre_id, studio_id, film_releaseDate, film_runtime)
            VALUES ('M3GAN', 'Gerard Johnstone', 
                    (SELECT genre_id FROM genre WHERE genre_name='Horror'), 
                    (SELECT studio_id FROM studio WHERE studio_name='Blumhouse Productions'),'2023', 102);
        """
        cursor.execute(insert_film_query)
        cnx.commit()  # Commit the transaction

        # Display films after insertion
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # Update the film 'Alien' to be a Horror film
        update_film_query = """
            UPDATE film
            SET genre_id = (SELECT genre_id FROM genre WHERE genre_name='Horror')  
            WHERE film_name = 'Alien';
        """
        cursor.execute(update_film_query)
        cnx.commit()  # Commit the transaction

        # Display films after update
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

        # Delete the movie 'Gladiator'
        delete_film_query = """
            DELETE FROM film
            WHERE film_name = 'Gladiator';
        """
        cursor.execute(delete_film_query)
        cnx.commit()  # Commit the transaction

        # Display films after deletion
        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    main()

