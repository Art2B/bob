import unittest

from context import bob
from bob import month_string_to_number

class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass
 
    def test_month_string_to_number(self):
        months_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for index, month in enumerate(months_list):
            self.assertEqual( month_string_to_number(month), index + 1)

        with self.assertRaises(ValueError):
            month_string_to_number('jfklqdsm')

        with self.assertRaises(TypeError):
            month_string_to_number(123)

if __name__ == '__main__':
    unittest.main()