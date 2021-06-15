from database import Database


class BiblioStream:
    def __init__(self, database: Database) -> None:
        self.db = database
        self.db.connect_to_db()
        print(
            "Please don't forget to call 'BiblioStream().end_session() after finishing your work'"
        )
    #USER SECTION
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
    
    # STREAMING SERVICE

    def get_stream_services_count(self) -> int:
        """
        This method returns the total number of streamingservices present in the database.
        """
        result = self.db.query_db("SELECT Count(*) FROM StreamingServices")
        # need to extract count value from list of tuple returned
        return int(result[0][0])
    
    def insert_streaming_service(self, streaming_name) -> str:
        """
        This method inserts a streaming service into the streaming service table.
        """
        streaming_count = self.get_stream_services_count

        streaming_insert = self.db.insert_into_db(
            f"INSERT INTO StreamingServices(name, id) \
            VALUES ('{streaming_name}', '{streaming_count}') RETURNING email"
        )

        return f"Inserted user with id = {streaming_count} and email = {streaming_name}"




    # Subscribes to 
    def get_subscribes_to(self, user_id) -> str:
        """
        This method returns a list of subscription services which the user is subscribed to 
        """

        result = self.db.query_db(f"SELECT streaming_name FROM SubscribesTo WHERE user_id='{user_id}'")
        return result

    # RATINGS

    
        

    def end_session(self) -> None:
        """
        This method is called to end the connection to the database.
        """
        self.db.close_db_connection()
