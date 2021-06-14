from database import Database


class BiblioStream:
    def __init__(self, database: Database) -> None:
        self.db = database
        self.db.connect_to_db()
        print(
            "Please don't forget to call 'BiblioStream().end_session() after finishing your work'"
        )

    def get_user_count(self) -> int:
        """
        This method returns the total number of users present in the database.
        """
        result = self.db.query_db("SELECT Count(*) FROM UserInfo")
        # need to extract count value from list of tuple returned
        return int(result[0][0])

    def insert_user(self, name, email, phone) -> str:
        """
        This method inserts a user into the database.
        The insert needs to happen on the UserInfo and UserContact tables.
        """
        user_count = self.get_user_count()

        user_email = self.db.insert_into_db(
            f"INSERT INTO UserContact(email, phone) \
            VALUES ('{email}', '{phone}') RETURNING email"
        )
        user_id = self.db.insert_into_db(
            f"INSERT INTO UserInfo(id, email, name) \
            VALUES ({user_count}, '{email}', '{name}') RETURNING id"
        )

        return f"Inserted user with id = {user_id} and email = {user_email}"

    def delete_user(self, email) -> None:
        """
        This method performs a cascade delete of a user from
        the UserInfo and UserContact tables.
        """
        self.db.delete_from_db(f"DELETE FROM UserContact WHERE email='{email}'")
        return f"Deleted user with email = {email} from db"

    def end_session(self) -> None:
        """
        This method is called to end the connection to the database.
        """
        self.db.close_db_connection()
