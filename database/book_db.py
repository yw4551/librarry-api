from database.db_connection import connection
from logs.logger import logger

class BookDB:
    def create_book(self, data: dict) -> int:
        logger.info("Creating a book.")
        if not data:
            logger.error("Some data is missing")
            raise ValueError("Some values missing.")

        logger.info("Executing SQL insert for new book.")
        sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"
        values = (data["title"], data["author"], data["genre"])
        book_id, _ = connection.send_request_to_db(sql, values)
        logger.info(f"Book created successfully with ID {book_id}.")
        return book_id

    def get_books(self) -> list:
        logger.info("Getting all books.")
        logger.info("Executing SQL selecting all books.")
        sql = "SELECT * FROM books"
        result = connection.send_request_without_commit(sql)
        logger.info("All books are shown.")
        return result

    def get_book(self, book_id: int) -> list:
        logger.info(f"Getting book with ID {book_id}.")
        logger.info("Executing SQL selecting a book.")
        sql = "SELECT * FROM books WHERE book_id = %s"
        values = (book_id, )
        result = connection.send_request_without_commit(sql, values)
        logger.info(f"Book with ID {book_id} is shown.")
        return result[0] if result else None

    def update(self, book_id: int, data: dict) -> bool:
        logger.info(f"Updating book with ID {book_id}")
        data_keys = [f"{key} = %s" for key in data.keys()]
        joined_keys = ", ".join(data_keys)
        logger.info("Executing SQL for updating a book.")
        sql = f"UPDATE books SET {joined_keys} WHERE book_id = %s"
        values = list(data.values()) + [book_id]
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Verifying the update.")
        return count_rows > 0

    def set_availability(self, book_id: int, val: bool, member_id: int):
        logger.info(f"Setting the availability of book {book_id} to {val}")
        logger.info("Executing SQL for updating the availability of a book.")
        sql = "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE book_id = %s"
        values = (val, member_id, book_id)
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Verifying changes.")
        return count_rows > 0

    def count_total_books(self):
        logger.info("Counting the num of books we have.")
        logger.info("Executing SQL counting the amount of books.")
        sql = "SELECT COUNT(*) FROM books"
        result = connection.send_request_without_commit(sql)
        logger.info("Getting the total number.")
        return result[0][0] if result and result[0] else 0

    def count_available_books(self):
        logger.info("Counting how many available books are they.")
        logger.info("Executing SQL counting available books.")
        sql = "SELECT COUNT(*)  FROM books WHERE is_available = %s"
        values = (True, )
        result = connection.send_request_without_commit(sql, values)
        logger.info("Getting the number.")
        return result[0][0] if result and result[0] else 0

    def count_borrowed_books(self):
        logger.info("Counting the amount of borrowed books.")
        logger.info("Executing SQL for counting borrowed books.")
        sql = "SELECT COUNT(*)  FROM books WHERE is_available = %s"
        values = (False,)
        result = connection.send_request_without_commit(sql, values)
        logger.info("Getting the number.")
        return result[0][0] if result and result[0] else 0

    def count_by_genre(self):
        logger.info("Counting books by genre.")
        logger.info("Executing SQL for counting books by genre.")
        sql = "SELECT genre, COUNT(*) FROM books GROUP BY genre"
        result = connection.send_request_without_commit(sql)
        logger.info("Getting the numbers.")
        return result if result else []

    def count_active_borrows_by_member(self, member_id: int):
        logger.info("Counting the number of active books the user has.")
        logger.info("Executing SQL counting books per user.")
        sql = "SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s"
        values = (member_id, )
        result = connection.send_request_without_commit(sql, values)
        logger.info("Getting the number.")
        return result[0][0] if result and result[0] else 0

book_db = BookDB()
