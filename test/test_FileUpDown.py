import os
import sys
import unittest
from unittest.mock import mock_open, patch

from FilesUpDown import readcred
from FilesUpDown import connection

os.chdir('../')
print(os.getcwd())


class NullDevice():
    """for capturing print() function putput"""
    def write(self, s): pass

    def flush(self): pass


class CredentialsTest(unittest.TestCase):

    original_stdout = sys.stdout

    def setUp(self):
        sys.stdout = NullDevice()  # redirect the real STDOUT
        print('dup')
        self.ConNelton = connection.Connection(
            host='host', user='user', passwd='p')
        self.Cred = readcred.ReadCredentials()

    def tearDown(self):
        sys.stdout = self.original_stdout

# here I've got problem with open file path.
# I think, that mocking is bad idea

    @patch('builtins.open', new_callable=mock_open, read_data='1')
    def test_read_credencials_flag_if_file_exists(self, mock_open):

        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')

        CredentialsDic = self.Cred.read_credencials()
        self.assertTrue(self.Cred.FTP_CRED,
                        'Flag of FTP_CRED should be true after reading')

    def test_read_credencials_flag_and_exception_if_file_not_present(self):
        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')

        os.chdir('../')
        CredentialsDic = self.Cred.read_credencials()
        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false after reading')


class ConnectionTest(unittest.TestCase):

    original_stdout = sys.stdout

    def setUp(self):
        sys.stdout = NullDevice()  # redirect the real STDOUT
        self.ConNelton = connection.Connection(
            host='host', user='user', passwd='p')

    def tearDown(self):
        sys.stdout = self.original_stdout

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
