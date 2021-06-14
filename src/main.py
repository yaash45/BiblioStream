import argparse
from database import Database


def main() -> None:
    # Create instance of argument parser
    parser = argparse.ArgumentParser(description="Pass database config")

    # Define argument for database config file path
    parser.add_argument("DatabaseConfigPath", metavar="path", type=str)

    # Parse provided argument from CLI
    args = parser.parse_args()

    if args.DatabaseConfigPath != None:
        # Create an instance of the Database
        db = Database(args.DatabaseConfigPath)

        # Connect to the database
        db.connect_to_db()

        # Test query. TODO Remove later
        print("Querying all countries from DB as a test")
        result = db.query_db("SELECT * FROM Country")
        print("Result:", result)

        # Close connection to database
        db.close_db_connection()


if __name__ == "__main__":
    main()
