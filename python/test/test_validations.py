import unittest

from python.src.put_user_lambda import is_date_of_birth_valid


class TestDateUtils(unittest.TestCase):

    def test_it_should_return_true_when_birthday_is_valid(self):
        # Given
        date_of_birth = "1988-08-10"

        # When
        is_valid = is_date_of_birth_valid(date_of_birth)

        # Then
        self.assertTrue(is_valid)

    def test_it_should_return_false_when_birthday_is_not_valid(self):
        # Given
        date_of_birth = "1988-08-10-2"

        # When
        is_valid = is_date_of_birth_valid(date_of_birth)

        # Then
        self.assertFalse(is_valid)

    def test_it_should_return_false_when_birthday_is_not_valid_v2(self):
        # Given
        date_of_birth = "1988-invalid"

        # When
        is_valid = is_date_of_birth_valid(date_of_birth)

        # Then
        self.assertFalse(is_valid)
