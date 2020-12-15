# Third party
import pg8000

# Custom
from config import (user, password, host, port, database)


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


    def createTableReviews(self, domain):
        """
            id SERIAL
            header NOT NULL
            body NOT NULL
            rating NOT NULL
            role empty string if empty
            date empty string if empty
            response TEXT
            source NOT NULL

        """
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS {domain}_reviews (
                            id SERIAL PRIMARY KEY,
                            header TEXT NOT NULL,
                            body TEXT NOT NULL,
                            rating REAL NOT NULL,
                            role TEXT,
                            date TEXT,
                            response TEXT,
                            source TEXT NOT NULL
                            );
                        ''')
        cursor.execute(
            f"SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
        results = cursor.fetchall()
        print(results)
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
        cursor.execute(
            f"SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
        results = cursor.fetchall()
        print(results)
        cursor.execute('COMMIT;')


    def intoReviews(self, domain, header, body, rating, role, date, response, source):
        """
             args = domain, header, body, rating, role, date, response, source
             domain = source / {table_name}_reviews
        """
        s = f"INSERT INTO {domain}_reviews(header, body, rating, role, date, response, source) VALUES ($${header}$$, $${body}$$, {rating}, $${role}$$, $${date}$$, $${response}$$, $${source}$$);"
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


    def dropTables(self, *args):
        """
            args = table name 1, table name 2 (optional) 
        """
        cursor.execute('BEGIN TRANSACTION;')
        try:
            s = f"DROP TABLE IF EXISTS {args[0]}, {args[1]} CASCADE;"
            cursor.execute(s)
        except:
            s = f"DROP TABLE IF EXISTS {args[0]} CASCADE;"
            cursor.execute(s)
        finally:
            cursor.execute(
                f"SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
            results = cursor.fetchall()
            print(results)
        cursor.execute('COMMIT;')