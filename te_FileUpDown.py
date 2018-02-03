import unittest
import FileUpDown
import json
import os
from mock import patch, Mock


class TestFileUpDown(unittest.TestCase):
    """docstring for TestFileUpDown"""

    def setUp(self):
        cred = {"NeltonHostName": "gsmdg.home.pl",
                     "NeltonUserName": "NeltonUser",
                     "NeltonPassword": "NeltonPass"}
        with open('../Cred/Test_NeltonFTP.json', 'w') as f:
            json.dump(cred, f)

    def tearDown(self):
        os.remove('../Cred/Test_NeltonFTP.json')

    def test_read_credencials(self, MockFTP, m_open):
        with open('../Cred/Test_NeltonFTP.json', 'r') as f:
            data = json.load(f)
            MockFTP.return_value = Mock()
            mock_ftp_obj = MockFTP()

            m_open.return_value = Mock()


if __name__ == '__main__':
    unittest.main()
