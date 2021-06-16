import argparse
from bibliostream import BiblioStream
from database import Database
import unittest

class querytest(unittest.TestCase):
# Create instance of argument parser
    
    def setUp(self) -> None:
        
        parser = argparse.ArgumentParser(description="Pass database config")

            # Define argument for database config file path
        parser.add_argument("DatabaseConfigPath", metavar="path", type=str)

            # Parse provided argument from CLI
        args = parser.parse_args()
        if args.DatabaseConfigPath != None:
                    # Create an instance of the Database
            self.db = Database(args.DatabaseConfigPath)
            self.bs = BiblioStream(self.db)
            
    

    def test_user_count(self):
        
        #self.bs.insert_user("Anam", "abc@ubc.ca", "1234567890")
        self.assertEqual(self.bs.get_user_count(),1, "Should be 1")
            



if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
