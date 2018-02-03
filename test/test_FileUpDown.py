import unittest
from unittest.mock import patch, mock_open
import sys
from FilesUpDown.FileUpDown import Connection
import FilesUpDown.FileUpDown as FileUpDown
from FilesUpDown.FileUpDown import ReadCredentials
import os

os.chdir('../')


class NullDevice():
    """for capturing print() function putput"""
    def write(self, s): pass

    def flush(self): pass


class CredentialsTest(unittest.TestCase):

    global original_stdout
    original_stdout = sys.stdout

    def setUp(self):
        self.ConNelton = Connection(host='host', user='user', password='p')
        sys.stdout = NullDevice()  # redirect the real STDOUT

    def tearDown(self):
        sys.stdout = original_stdout

# here I've got problem with open file path.
# I think, that mocking is bad idea

    @patch('builtins.open', new_callable=mock_open, read_data='1')
    def test_read_credencials_flag_if_file_exists(self, mock_open):
        self.assertFalse(FileUpDown.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')
        ReadCredentials.read_credencials()
        self.assertTrue(FileUpDown.FTP_CRED,
                        'Flag of FTP_CRED should be true after reading')

    def test_read_credencials_flag_and_exception_if_file_not_present(self):
        self.assertFalse(FileUpDown.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')
        os.chdir('../')
        ReadCredentials.read_credencials()

        self.assertFalse(FileUpDown.FTP_CRED,
                         'Flag of FTP_CRED should be false after reading')
        os.chdir('./FilesUpDown')


class ConnectionTest(unittest.TestCase):

    global original_stdout
    original_stdout = sys.stdout

    def setUp(self):
        self.ConNelton = Connection(host='host', user='user', password='p')
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
