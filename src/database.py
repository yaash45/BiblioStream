import psycopg2
import yaml
from psycopg2 import Error


class Database:
    """
    This class represents an abstraction of the database.
    It can be used to connect to a database and run queries on it.
    """

    def __init__(self, configpath: str) -> None:
        """
        Creates an instance of Database. It is responsible for parsing the
        database credentials from the provided yaml file in the configpath.
        """
        self._parse_and_set_config(configpath=configpath)

    def _parse_and_set_config(self, configpath: str) -> None:
        """
        Parses the YAML file at configpath for the database credentials.
        """
        with open(configpath, "r") as config:
            try:
                loaded_config = yaml.safe_load(config)

                if loaded_config["postgres"] != None:
                    self.db_config_map = loaded_config["postgres"]
                    self.host = self.db_config_map["host"]
                    self.port = self.db_config_map["port"]
                    self.database = self.db_config_map["database"]
                    self.user = self.db_config_map["user"]
                    self.password = self.db_config_map["password"]
            except:
                print("Error parsing config")

    def get_db_config_map(self) -> map:
        """
        Convenient method added for debugging.
        It can be used to verify if configuration is being parsed correctly.
        """
        return self.db_config_map

    def connect_to_db(self) -> None:
        """
        Creates a connection to the database.
        """
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
            )

        except (Exception, Error) as error:
            print("Could not connect to database. Error =", error)
        finally:
            print("Successfully connected to database")

    def query_db(self, query_string: str) -> list:
        """
        Runs provided query_string as a query on the database
        and returns a list containing the results.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_string)
            result = cursor.fetchall()
            cursor.close()
            return result
        except (Exception, Error) as error:
            print("Could not query db. Error =", error)

    def insert_into_db(self, query_string: str) -> str:
        """
        Inserts provided query_string as a query on the database
        and returns a value specified in query.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_string)
            result = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return result
        except (Exception, Error) as error:
            print("Could not insert into db. Error =", error)

    def delete_from_db(self, query_string: str) -> None:
        """
        Deletes row from db based on provided query_string
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_string)
            self.connection.commit()
            cursor.close()
        except (Exception, Error) as error:
            print("Could not delete from db. Error =", error)

    def update_in_db(self, query_string: str) -> None:
        """
        Updates row in db based on provided query_string
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_string)
            self.connection.commit()
            cursor.close()
        except (Exception, Error) as error:
            print("Could not update in db. Error =", error)

    def close_db_connection(self) -> None:
        """
        Closes connection to the database.
        """
        self.connection.close()
        print("Closed connection to database")
