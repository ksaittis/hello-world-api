import unittest

from python.src.models.User import User


class TestUser(unittest.TestCase):

    def test_it_should_be_able_to_create_user_from_event(self):
        # Given
        expected_username = "Kostas"
        event = {"pathParameters": {"username": expected_username}, "body": "{\"dateOfBirth\": \"1980-08-10\"}"}

        # When
        user = User.from_event(event)

        # Then
        self.assertEqual(user.username.value, expected_username)
        self.assertEqual(user.birthdate.value, "1980-08-10")
        self.assertTrue(user.is_username_valid())
        self.assertTrue(user.is_birthdate_valid())

    def test_it_should_be_able_to_create_user_from_event_without_body(self):
        # Given
        expected_username = "Kostas"
        event = {"pathParameters": {"username": expected_username}, "body": None}

        # When
        user = User.from_event(event)

        # Then
        self.assertEqual(user.username.value, expected_username)
        self.assertTrue(user.is_username_valid())
        self.assertFalse(user.is_birthdate_valid())
