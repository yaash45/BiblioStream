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
        
        
        self.assertEqual(self.bs.get_user_count(),3, "Should be 1")

  #def test_delete_user(self):
        
        #self.bs.insert_user("Anam", "abc@anam.ca", "1234567890")
        #self.assertEqual(self.bs.get_user_count(),2, "Should be 2")
        #self.bs.delete_user("abc@anam.ca")
        #self.assertEqual(self.bs.get_user_count(),1, "Should be 1")
    
    def test_get_stream_service_count(self):
        self.assertEqual(self.bs.get_stream_services_count(),1, "Should be 1")
    
    def test_all_streaming_service(self):
        
        self.assertEqual(self.bs.all_streaming_service(), "Netflix", "Should list all")

    

    def test_max_cert(self):
        
        self.assertEqual(self.bs.max_certifications(), "blackfriday", "Should be correct")

    
    def test_select_certifications(self):
        self.assertEqual(self.bs.select_certification("nsfw"), "jupiter", "KdotxJcole")

    def test_aggregate(self):
        self.assertEqual(self.bs.aggregate_movie_length("avg"), 200, "Lowkey these movies hella long")

    def test_project_series(self):
        self.assertEqual(self.bs.project_series(), [('boondocks', 4, 24), ('suits', 8, 14)], "f(x)")



        



if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
