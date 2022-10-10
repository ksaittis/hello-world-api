import os

import boto3

from python.src.models.User import User


class DynamoDbOperationUnsuccessfulError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class DynamoDbHelper:

    def __init__(self):
        self.dynamodb_client = boto3.client('dynamodb', region_name=os.getenv('REGION', 'eu-west-1'))

    def put_user(self, user: User) -> None:
        try:
            dynamodb_put_item_response = self.dynamodb_client.put_item(
                TableName=os.environ['DYNAMODB_TABLE_NAME'],
                Item={
                    'username': {
                        'S': user.username.value
                    },
                    'dateOfBirth': {
                        'S': user.birthdate.value
                    }
                }
            )
            if dynamodb_put_item_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return

            raise DynamoDbOperationUnsuccessfulError

        except Exception as error:
            raise error

    def get_user(self, user: User) -> User:
        try:
            dynamodb_get_item_response = self.dynamodb_client.get_item(
                TableName=os.environ['DYNAMODB_TABLE_NAME'],
                Key={
                    'username': {
                        'S': user.username.value
                    }
                }
            )
            if dynamodb_get_item_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                if 'Item' in dynamodb_get_item_response and 'dateOfBirth' in dynamodb_get_item_response['Item']:
                    date_of_birth = dynamodb_get_item_response['Item']['dateOfBirth']['S']
                    return User(username=user.username.value, date_of_birth=date_of_birth)

                raise UserNotFoundError
            raise DynamoDbOperationUnsuccessfulError

        except Exception as error:
            raise error
