import unittest

from python.src.models.username import *


class TestBirthdate(unittest.TestCase):

    def test_it_should_return_true_if_username_is_valid(self):
        # Given
        username = Username("Kostas")

        # When
        self.assertTrue(username.is_valid())

    def test_it_should_return_false_if_username_is_not_valid(self):
        # Given
        username_with_numbers = Username("Kostas123")
        username_with_just_numbers = Username("123")
        username_contains_hyphen = Username("Kostas-World")

        # When
        self.assertFalse(username_with_numbers.is_valid())
        self.assertFalse(username_with_just_numbers.is_valid())
        self.assertFalse(username_contains_hyphen.is_valid())
