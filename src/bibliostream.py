from typing import DefaultDict
from database import Database


class BiblioStream:
    def __init__(self, database: Database) -> None:
        self.db = database
        self.db.connect_to_db()
        print(
            "Please don't forget to call 'BiblioStream().end_session() after finishing your work'"
        )

    # UserSection
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

    def delete_user(self, email) -> str:
        """
        This method performs a cascade delete of a user from
        the UserInfo and UserContact tables.
        """

        self.db.delete_from_db(f"DELETE FROM UserContact WHERE email='{email}'")
        return f"Deleted user with email = {email} from db"

    def update_user_phone(self, email, phone) -> str:
        """
        This method updates a user's phone number for a given email
        """

        query = f" UPDATE UserContact \
                SET phone = '{phone}' \
                WHERE email = '{email}'"

        self.db.update_in_db(query)
        return f"Updated user with email = {email} to have phone number {phone}"

    # StreamingServices
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

        streaming_count = self.get_stream_services_count()

        streaming_id = self.db.insert_into_db(
            f"INSERT INTO StreamingServices(name, id) \
            VALUES ('{streaming_name}', '{streaming_count}') RETURNING id"
        )

        return f"Inserted service with id = {streaming_id} and name = {streaming_name}"

    def all_streaming_service(self) -> str:
        """
        This method returns all of the streaming services available within the website

        (Projection criteria)
        """

        string_names = self.db.query_db("SELECT id, name FROM StreamingServices")

        def listToString(s):

            # initialize an empty string
            str1 = ""

            # traverse in the string
            for ele in s:
                str1 += ele

            # return string
            return str1

        output = listToString([x[1] for x in string_names])
        return output

    # SubscribesTo
    def get_subscribes_to(self, user_id) -> str:
        """
        This method returns a list of subscription services which the user is subscribed to
        """

        result = self.db.query_db(
            f"SELECT streaming_name FROM SubscribesTo WHERE user_id='{user_id}'"
        )
        return result

    def get_subcribes_to_count(self, user_id) -> int:
        """
        This method returns the number of subscription services to which the user is subscribed to
        """

        result = self.db.query_db(
            f"SELECT Count(*) FROM SubscribesTO WHERE user_id='{user_id}'"
        )
        return int(result[0][0])

    # Certifications
    def insert_cert(self, cert_name) -> str:
        """
        This method inserts a streaming service into the streaming service table.
        """

        cert_insert = self.db.insert_into_db(
            f"INSERT INTO Certifications(name) \
            VALUES ('{cert_name}') RETURNING name"
        )

        return f"Inserted cert with name = {cert_insert}"

    def max_certifications(self):
        """
        This method returns the videomedia with the most certifications
        (Nested AGGREGATE) criteria (not tested yet) (need to populate respective tables)
        """

        max_certs = self.db.query_db(
            "SELECT videomedia_name FROM \n"+
            "(SELECT videomedia_name, certCount FROM \n"  +
            "(SELECT videomedia_name, Count(*) AS certCount \n"+ 
             "from Receives \n" +
            "GROUP BY videomedia_name) AS derivedTable \n"+
			"ORDER by certCount DESC) As orderedTable \n"+
			"LIMIT 1;"
        )
        return max_certs[0][0]
    # Video Media
    def insert_VideoMedia(self, name):
        """Thsis method will insert video media into Database given name
        """
        video = streaming_id = self.db.insert_into_db(
            f"INSERT INTO VideoMedia(name) \
            VALUES ('{name}') RETURNING name"
        )
        return video
        

    def select_certification(self, selection: str) -> list:
        """
        Selects certifications based on user input (Join criteria)
        """
        query = f"SELECT v.name, c.name \
            FROM Receives r, Certifications c, VideoMedia v\
            WHERE r.certifications_name = c.name AND r.videomedia_name = v.name AND LOWER(c.name) = LOWER('{selection}')"
        
        return self.db.query_db(query)

    # Movies

    def aggregate_movie_length(self, agg_func:str):
        """
        This method returns the average length/running time of movies
        (Aggregation Criteria)
        """

        agg_result = self.db.query_db(
            f"SELECT {agg_func}(M.length) \
            FROM Movies M"
        )
        return int(agg_result[0][0])

    # Series

    def select_series(self, criteria) -> list:
        """
        This method selects rows based on the given criteria
        from the Series table. (Selection Critieria)
        """

        if criteria != None or criteria != "":
            query = f"SELECT name, seasons, episodes\
                    FROM Series\
                    WHERE {criteria}"

            return self.db.query_db(query)
        else:
            return []

    def project_series(self, seasons=True, episodes=True) -> list:
        """
        This method projects selective rows from the Series Table.
        """

        if seasons == False and episodes == False:
            raise (
                Exception(
                    "Please select at least one of the seasons and episodes to be true"
                )
            )
        query = "SELECT DISTINCT name"

        if seasons:
            query += ", seasons"

        if episodes:
            query += ", episodes"

        query += f" FROM Series"

        return self.db.query_db(query)

    # Genre
    def insert_genre(self, genre_name) -> str:
        """
        This method inserts a genre into the table
        """

        genre_insert = self.db.insert_into_db(
            f"INSERT INTO Genre(name) \
            VALUES ('{genre_name}') RETURNING name"
        )

        return f"Inserted genre with name = {genre_insert}"

    # Receives
    def insert_receives(self, videomedia_name, certifications_name) -> str:
        """
        This method inserts into the receives table where x video media receives y certificate
        """

        receives_insert = self.db.insert_into_db(
            f"INSERT INTO Receives \
                VALUES ('(SELECT name FROM VideoMedia WHERE name = {videomedia_name})', '(SELECT name FROM Certifications WHERE name = {certifications_name})') \
                    RETURNING videomedia_name, certifications_name "
        )
        return f"Inserting {receives_insert}"
    
    # Division Criteria

    def has_all_streaming(self) -> str:
        """
        This method fulfills the division criteria of the rubric; this returns the videomedia which is in every streaming service

        """
        videoMediaName = self.db.query_db(f"SELECT name")

    def end_session(self) -> None:
        """pipenv install
        
        This method is called to end the connection to the database.
        """
        self.db.close_db_connection()
