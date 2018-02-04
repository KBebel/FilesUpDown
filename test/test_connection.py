import unittest
from unittest.mock import patch
import sys
from FilesUpDown.connection import Connection

import os

os.chdir('../')


class NullDevice():
    """for capturing print() function putput"""
    def write(self, s): pass

    def flush(self): pass


class ConnectionTest(unittest.TestCase):

    global original_stdout
    original_stdout = sys.stdout

    def setUp(self):
        self.ConNelton = Connection(host='host', user='user', passwd='p')
        sys.stdout = NullDevice()  # redirect the real STDOUT

    def tearDown(self):
        sys.stdout = original_stdout

    @patch('ftplib.FTP', autospec=True)
    def test_connect_func(self, mock_ftp_constructor):
        self.mock_ftp = mock_ftp_constructor.return_value
        self.assertFalse(self.ConNelton.bool_connected_with_ftp,
                         'Flag of connected_with_ftp should be\
                          false before connecting')
        self.ConNelton.connect_with_ftp()

        mock_ftp_constructor.assert_called_with('host', timeout=10)
        self.assertTrue(self.mock_ftp.login.called)
        self.assertTrue(self.ConNelton.bool_connected_with_ftp,
                        'Flag of connected_with_ftp should be\
                         true after connecting')


if __name__ == '__main__':
    unittest.main()
