import unittest
from unittest.mock import patch
from FilesUpDown.calc import Calculator as cac
from FilesUpDown.calc import my_function


# if "C:\\Users\\Karol Bebel\\Programming" not in sys.path:
#     sys.path.append("C:\\Users\\Karol Bebel\\Programming")


class TestCalculator(unittest.TestCase):

    # def setUp(self):
    #     self.calc = Calculator()

    # def test_sum(self):
    #     self.assertEqual(self.calc.sum(2, 3), 5)

    @patch('FilesUpDown.calc.Calculator.sum', return_value = 50)
    def test_sum(self, sum):
        self.assertEqual(sum(2, ), 50)


class TestCalc(unittest.TestCase):

    # @mock.patch('calc.os')
    # # @mock.patch('calc.os.path')
    # def test_rm(self, mock_os):
    #     mock_os.path.isfile.return_value = False

    #     rm("any path")

    #     self.assertFalse(mock_os.remove.called, "Failed ")
    #     mock_os.remove.assert_not_called()

    #     mock_os.path.isfile.return_value = True

    #     rm('any path')

    #     mock_os.remove.assert_called_with('any path')

    def testMyFunction(self):
        """
        my_function() does not crash
        """
        my_function(5)

    def test_true_and_test_false(self):
        """
        Using assertTru and False test things
        """
        self.assertTrue(my_function(5) == 10)
        self.assertFalse(my_function(5) == 9)

    def test_special_zero(self):
        """my_function(0) is special, and returns 100
        """
        x = my_function(0)
        if x != 100:
            self.fail("Zero is special, my_funcion(0) didn't return 100!")


if __name__ == '__main__':
    unittest.main()
