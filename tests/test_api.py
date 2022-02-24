import unittest
import api

class test_api(unittest.TestCase):
    def TestConnection(self):
        self.assertFalse(api.Connect2Api('') == None)

if __name__ == "__main__":
    unittest.main()