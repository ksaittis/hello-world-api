import unittest
import boto3
import moto
from botocore.exceptions import ClientError

from python.src.models.User import User
from python.src.utils.dynamodb_helper import DynamoDbHelper, UserNotFoundError, DynamoDbOperationUnsuccessfulError


@moto.mock_dynamodb
class TestDynamo(unittest.TestCase):

    def test_it_should_be_able_to_put_and_retrieve_user(self):
        # Given
        username = "Kostas"
        date_of_birth = "1987-01-01"
        expected_user = User(username, date_of_birth)

        dynamodb = boto3.resource('dynamodb', 'eu-west-1')
        dynamodb.create_table(
            TableName='Users',
            BillingMode='PAY_PER_REQUEST',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
        )

        # When
        db = DynamoDbHelper()
        db.put_user(User(username, date_of_birth), 'Users')
        actual_user = db.get_user(User(username))

        # Then
        self.assertEqual(actual_user.username.value, expected_user.username.value)
        self.assertEqual(actual_user.birthdate.value, expected_user.birthdate.value)

    def test_it_should_raise_exception_when_user_not_found(self):
        # Given
        dynamodb = boto3.resource('dynamodb', 'eu-west-1')
        dynamodb.create_table(
            TableName='Users',
            BillingMode='PAY_PER_REQUEST',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
        )

        # When
        db = DynamoDbHelper()

        # Then
        self.assertRaises(UserNotFoundError, lambda: db.get_user(User("unknown")))

    def test_it_should_raise_client_error_when_table_not_found_while_putting_user(self):
        # Given
        dynamodb = boto3.resource('dynamodb', 'eu-west-1')
        dynamodb.create_table(
            TableName='WrongTable',
            BillingMode='PAY_PER_REQUEST',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
        )

        # When
        db = DynamoDbHelper()

        # Then
        self.assertRaises(ClientError, lambda: db.put_user(User("Kostas", "1990-01-01"), table_name="CorrectTable"))

    def test_it_should_raise_client_error_when_table_not_found_while_getting_user(self):
        # Given
        dynamodb = boto3.resource('dynamodb', 'eu-west-1')
        dynamodb.create_table(
            TableName='WrongTable',
            BillingMode='PAY_PER_REQUEST',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
        )

        # When
        db = DynamoDbHelper()

        # Then
        self.assertRaises(ClientError, lambda: db.get_user(User("Kostas", "1990-01-01"), table_name="CorrectTable"))
