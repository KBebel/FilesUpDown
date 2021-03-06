import os
import sys
import unittest
from unittest.mock import mock_open, patch

from FilesUpDown.readcred import ReadCredentials

os.chdir('../')


class NullDevice():
    """for capturing print() function putput"""
    def write(self, s): pass

    def flush(self): pass


class CredentialsTest(unittest.TestCase):

    original_stdout = sys.stdout

    def setUp(self):
        sys.stdout = NullDevice()  # redirect the real STDOUT
        self.Cred = ReadCredentials()

    def tearDown(self):
        sys.stdout = self.original_stdout

# here I've got problem with open file path.
# I think, that mocking is bad idea

    @patch('builtins.open', new_callable=mock_open, read_data='1')
    def test_read_credencials_flag_if_file_exists(self, mock_open):
        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')
        self.Cred.read_credencials()
        self.assertTrue(self.Cred.FTP_CRED,
                        'Flag of FTP_CRED should be true after reading')

    def test_read_credencials_flag_and_exception_if_file_not_present(self):
        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false before reading')
        os.chdir('../')
        self.Cred.read_credencials()

        self.assertFalse(self.Cred.FTP_CRED,
                         'Flag of FTP_CRED should be false after reading')


if __name__ == '__main__':
    unittest.main()
