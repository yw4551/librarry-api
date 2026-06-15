from database.db_connection import connection
from logs.logger import logger

class Member:
    def create(self, data: dict) -> int:
        logger.info("Creating a member.")
        if not data:
            logger.error("You are missing some data.")
            raise ValueError("Some values missing.")
        logger.info("Executing SQL insert for new member.")
        sql = "INSERT INTO members (name, email) VALUES (%s, %s)"
        values = (data["name"], data["email"])
        member_id, _ = connection.send_request_to_db(sql, values)
        logger.info(f"The member was created with ID {member_id}")
        return member_id

    def get_members(self) -> list:
        logger.info("Getting all members.")
        logger.info("Executing SQL for selecting all members.")
        sql = "SELECT * FROM members"
        logger.info("All members are shown.")
        return connection.send_request_without_commit(sql)

    def get_member(self, member_id: int) -> list:
        logger.info(f"Getting member with ID {member_id}")
        logger.info("Executing SQL for selecting a member.")
        sql = "SELECT * FROM members WHERE member_id = %s"
        values = (member_id, )
        result = connection.send_request_without_commit(sql, values)
        logger.info(f"Showing member with ID {member_id}")
        return result[0] if result else None

    def update(self, member_id: int, data: dict):
        logger.info(f"Updating member with ID {member_id}.")
        data_keys = [f"{key} = %s" for key in data.keys()]
        joined_keys = ", ".join(data_keys)
        logger.info("Executing SQL for updating a member.")
        sql = f"UPDATE members SET {joined_keys} WHERE member_id = %s"
        values = list(data.values()) + [member_id]
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Validating changes.")
        return count_rows > 0

    def deactivate(self, member_id: int):
        logger.info(f"Deactivating member {member_id}")
        logger.info("Executing SQL for deactivating a member.")
        sql = "UPDATE members SET is_active = %s WHERE member_id = %s"
        values = (False, member_id)
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Validating changes.")
        return count_rows > 0

    def activate(self, member_id: int):
        logger.info(f"Activating member {member_id}.")
        logger.info("Executing SQL to activate a member.")
        sql = "UPDATE members SET is_active = %s WHERE member_id = %s"
        values = (True, member_id)
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Validating changes.")
        return count_rows > 0

    def increment_borrows(self, member_id: int):
        logger.info(f"Increment borrows for member {member_id}")
        logger.info("Executing SQL to increment a members borrows.")
        sql = "UPDATE members SET total_borrows = total_borrows + 1 WHERE member_id = %s"
        values = (member_id, )
        _, count_rows = connection.send_request_to_db(sql, values)
        logger.info("Validating changes.")
        return count_rows > 0

    def count_actives(self):
        logger.info("Counting the amount of active members.")
        logger.info("Executing SQL to count active members.")
        sql = "SELECT COUNT(is_active) FROM members WHERE is_active = %s"
        values = (True, )
        result = connection.send_request_without_commit(sql, values)
        logger.info("Getting the number.")
        return result[0][0] if result and result[0] else 0

    def get_top_member(self):
        logger.info("Getting the member with the top borrows.")
        logger.info("Executing SQL to get top member.")
        sql = "SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1"
        result = connection.send_request_without_commit(sql)
        logger.info("Showing the member with the top borrows.")
        return result[0] if result else None


member_db = Member()
