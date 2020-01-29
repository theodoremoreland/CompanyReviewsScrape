import pg8000
from config2 import (user, password, host, port, database)



class DB:

    def __init__(self):
        pass

    def connect(self):
        global connection
        global cursor

        connection = pg8000.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=int(port),
                                    database=database)

        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    def createTableReviews(self):
        """
            id SERIAL
            header NOT NULL
            body NOT NULL
            rating NOT NULL
            role empty string if empty
            date empty string if empty
            source NOT NULL
            
        """
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS reviews (
                            id SERIAL PRIMARY KEY,
                            header TEXT NOT NULL,
                            body TEXT NOT NULL,
                            rating INTEGER NOT NULL,
                            role TEXT,
                            date TEXT,
                            source TEXT NOT NULL
                            );
                        ''')
        cursor.execute('COMMIT;')

    def createTableResponses(self):
        """
            id AUTO_INCREMENT
            body NOT NULL
            role empty string if empty
            date empty string if empty
            source NOT NULL
            post_id NOT NULL FOREIGN KEY

        """
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS responses (
                            id SERIAL PRIMARY KEY,
                            body TEXT NOT NULL,
                            role TEXT NOT NULL,
                            date TEXT,
                            source TEXT NOT NULL,
                            post_id INTEGER REFERENCES reviews(id)
                            );
                        ''')
        cursor.execute('COMMIT;')



    def intoReviews(self, header, body, rating, role, date, source):
        s = f"INSERT INTO profile(header, body, rating, role, date, source) VALUES ('{header}', '{body}', {rating}, '{role}', '{date}', '{source}');"
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(s)
        cursor.execute('COMMIT;')


    def intoResponses(self, body, role, date, source, post_id):
        s = f"INSERT INTO posts(body, role, date, source, post_id) VALUES ('{body}', '{role}', '{date}', '{source}', {post_id});"
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(s)
        cursor.execute('COMMIT;')

    def select(self):
        try:
            cursor.execute("SELECT * from profile;")
            record = cursor.fetchall()
            print(record)
        except Exception as e:
            print(e)
        try:
            cursor.execute("SELECT * from posts;")
            record = cursor.fetchall()
            print(record)
        except Exception as e:
            print(e)
