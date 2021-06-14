from database import Database


class BiblioStream:
    def __init__(self, database: Database) -> None:
        self.db = database
        self.db.connect_to_db()

    def get_user_count(self) -> int:
        result = self.db.query_db("SELECT Count(*) FROM UserInfo")
        # need to extract count value from list of tuple returned
        return int(result[0][0])

    def insert_user(self, name, email, phone) -> str:
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

    def end_session(self) -> None:
        self.db.close_db_connection()
