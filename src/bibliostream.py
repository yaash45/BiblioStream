from database import Database


class BiblioStream:
    def __init__(self, database: Database) -> None:
        self.db = database
        self.db.connect_to_db()

    def insert_user(self, name, email, phone) -> str:
        user_email = self.db.insert_into_db(
            f"INSERT INTO UserContact(email, phone) \
            VALUES ('{email}', '{phone}') RETURNING email"
        )
        user_id = self.db.insert_into_db(
            f"INSERT INTO UserInfo(id, email, name) \
            VALUES ({0}, '{email}', '{name}') RETURNING id"
        )

        return f"Inserted user with id = {user_id} and email = {user_email}"

    def end_session(self) -> None:
        self.db.close_db_connection()
