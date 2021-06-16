import argparse
from bibliostream import BiblioStream
from database import Database
import unittest


# Create instance of argument parser
parser = argparse.ArgumentParser(description="Pass database config")

    # Define argument for database config file path
parser.add_argument("DatabaseConfigPath", metavar="path", type=str)

    # Parse provided argument from CLI
args = parser.parse_args()

if args.DatabaseConfigPath != None:
        # Create an instance of the Database
    db = Database(args.DatabaseConfigPath)
    bs = BiblioStream(db)
        
    

def test_user_count():
    bs.insert_user("Yaash", "abc@ubc.ca", "1234567890")
    assert bs.get_user_count() == 2, "Should be 1"
        



if __name__ == "__main__":
    test_user_count()
    bs.end_session()
