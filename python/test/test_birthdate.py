import unittest

from freezegun import freeze_time
from freezegun.api import FakeDate

from python.src.models.Birthdate import *


class TestBirthdate(unittest.TestCase):

    @freeze_time("2022-08-10")
    def test_it_should_return_true_if_birthday_is_valid(self):
        # Given
        birthdate = Birthdate("2020-08-01")

        # When
        is_valid = birthdate.is_valid()

        # Then
        self.assertTrue(is_valid)

    @freeze_time("2022-08-10")
    def test_it_should_return_false_if_birthday_is_not_valid(self):
        # Given
        birthdate_in_future = Birthdate("2022-08-11")
        invalid_format_birthday = Birthdate("2022-08-01-02")
        letters_only_birthday = Birthdate("hello-world")

        # Then
        self.assertFalse(birthdate_in_future.is_valid())
        self.assertFalse(invalid_format_birthday.is_valid())
        self.assertFalse(letters_only_birthday.is_valid())

    @freeze_time("2022-08-10")
    def test_it_should_return_true_when_birthday_is_today(self):
        # Given
        birthdate = Birthdate("1988-08-10")

        # When

        # Then
        self.assertTrue(birthdate.is_today())

    @freeze_time("2022-08-10")
    def test_it_should_return_false_when_birthday_is_not_today(self):
        # Given
        birthdate = Birthdate("1988-08-11")

        # When

        # Then
        self.assertFalse(birthdate.is_today())

    @freeze_time("2022-01-01")
    def test_it_should_calculate_next_birthday_in_couple_of_days(self):
        # Given
        expected_birthday = FakeDate(2022, 1, 10)
        birthdate = Birthdate("1988-01-10")

        # When
        actual_birthday = birthdate.get_next_birthday()

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-08-10")
    def test_it_should_calculate_next_birthday_for_next_year(self):
        # Given
        expected_birthday = FakeDate(2023, 1, 1)
        birthdate = Birthdate("1988-01-01")

        # When
        actual_birthday = birthdate.get_next_birthday()

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-01-01")
    def test_it_should_calculate_next_birthday_for_same_year(self):
        # Given
        expected_birthday = FakeDate(2022, 2, 1)
        birthdate = Birthdate("1988-02-01")

        # When
        actual_birthday = birthdate.get_next_birthday()

        # Then
        self.assertEqual(expected_birthday, actual_birthday)

    @freeze_time("2022-01-01")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_same_year(self):
        # Given
        birthdate = Birthdate("1988-02-01")
        expected_days_until_birthday = 31

        # When
        actual_days_until_next_birthday = birthdate.get_days_until_next_birthday()

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)

    @freeze_time("2022-02-01")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_next_year(self):
        # Given
        birthdate = Birthdate("1988-01-01")
        expected_days_until_birthday = 334

        # When
        actual_days_until_next_birthday = birthdate.get_days_until_next_birthday()

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)

    @freeze_time("2022-10-08")
    def test_it_should_calculate_days_until_next_birthday_when_birthday_next_year_v2(self):
        # Given
        birthdate = Birthdate("1988-01-01")
        expected_days_until_birthday = 85

        # When
        actual_days_until_next_birthday = birthdate.get_days_until_next_birthday()

        # Then
        self.assertEqual(expected_days_until_birthday, actual_days_until_next_birthday)
