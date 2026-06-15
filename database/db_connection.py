import mysql.connector
from logs.logger import logger


class Connector:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )
        self.create_database_if_not_exists()

    def start_cursor(self):
        self.cursor = self.conn.cursor()
        logger.info("Cursor started successfully.")

    def close_cursor(self):
        self.cursor.close()
        logger.info("Cursor closed successfully.")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logger.info("Connection to DB closed successfully.")

    def create_database_if_not_exists(self):
        self.start_cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        logger.info(f"DB {self.database} created successfully.")
        self.cursor.execute(f"USE {self.database}")
        logger.info(f"Using {self.database}.")
        self.close_cursor()

    def create_table_if_not_exists(self, name: str, cols: str):
        self.start_cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}({cols})")
        logger.info(f"Table {name} created successfully.")
        self.conn.commit()
        logger.info("Changes committed successfully.")
        self.close_cursor()

    def send_request_to_db(self, sql_request: str, params: tuple = None):
        self.start_cursor()
        self.cursor.execute(sql_request, params)
        self.conn.commit()
        logger.info("Changes committed successfully.")
        last_id = self.cursor.lastrowid
        count_rows = self.cursor.rowcount
        self.close_cursor()
        return last_id, count_rows

    def send_request_without_commit(self, sql_request: str, params: tuple = None):
        self.start_cursor()
        self.cursor.execute(sql_request, params)
        result = self.cursor.fetchall()
        self.close_cursor()
        return result


connection = Connector("127.0.0.1", "root", "secret", "library_db", 3306)
connection.create_table_if_not_exists(
    "books",
    """
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
    is_available BOOLEAN DEFAULT TRUE,
    borrowed_by_member_id INT DEFAULT NULL
""",
)
connection.create_table_if_not_exists(
    "members",
    """
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    total_borrows INT DEFAULT 0
"""
)
