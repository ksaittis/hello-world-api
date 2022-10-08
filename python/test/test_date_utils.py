import unittest

from freezegun import freeze_time
from freezegun.api import FakeDate

from python.src.get_user_lambda import is_birthday_today, get_next_birthday, get_days_until_next_birthday


class TestDateUtils(unittest.TestCase):

    @freeze_time("2022-08-10")
    def test_it_should_return_true_when_birthday_is_today(self):
        # Given
        date_of_birth = "1988-08-10"

        # When

        # Then
        self.assertTrue(is_birthday_today(date_of_birth))

    @freeze_time("2022-08-10")
    def test_it_should_return_false_when_birthday_is_not_today(self):
        # Given
        date_of_birth = "1988-08-11"

        # When

        # Then
        self.assertFalse(is_birthday_today(date_of_birth))

    @freeze_time("2022-01-01")
    def test_it_should_calculate_next_birthday_in_couple_of_days(self):
        # Given
        expected_birthday = FakeDate(2022, 1, 10)
        date_of_birth = "1988-01-10"

        # When
        actual_birthday = get_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-08-10")
    def test_it_should_calculate_next_birthday_for_next_year(self):
        # Given
        expected_birthday = FakeDate(2023, 1, 1)
        date_of_birth = "1988-01-01"

        # When
        actual_birthday = get_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-01-01")
    def test_it_should_calculate_next_birthday_for_same_year(self):
        # Given
        expected_birthday = FakeDate(2022, 2, 1)
        date_of_birth = "1988-02-01"

        # When
        actual_birthday = get_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-01-01")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_same_year(self):
        # Given
        date_of_birth = "1988-02-01"
        expected_days_until_birthday = 31

        # When
        actual_days_until_next_birthday = get_days_until_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)

    @freeze_time("2022-02-01")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_next_year(self):
        # Given
        date_of_birth = "1988-01-01"
        expected_days_until_birthday = 334

        # When
        actual_days_until_next_birthday = get_days_until_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)

    @freeze_time("2022-10-08")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_next_year_v2(self):
        # Given
        date_of_birth = "1988-01-01"
        expected_days_until_birthday = 85

        # When
        actual_days_until_next_birthday = get_days_until_next_birthday(date_of_birth)

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)
