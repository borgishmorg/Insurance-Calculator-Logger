import psycopg2

DATABASE = 'calc_log'
USER = 'postgres'
PASSWORD = 'docker'
HOST = '0.0.0.0'


class DBConnection:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                database=DATABASE,
                user=USER,
                password=PASSWORD,
                host=HOST
            )
            self.cursor = self.conn.cursor()
            self.create_tables()
        except psycopg2.DatabaseError as error:
            print(error)
            exit(1)

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS log(
            id serial PRIMARY KEY,
            datetime TIMESTAMP,
            tag VARCHAR(5),
            msg VARCHAR(500)
        );
        """)
        self.conn.commit()

    def insert(self, datetime, tag, msg):
        msg = msg.decode('utf-8')
        self.cursor.execute('INSERT INTO log(datetime, tag, msg) VALUES (%s, %s, %s)', (datetime, tag, msg))
        self.conn.commit()
