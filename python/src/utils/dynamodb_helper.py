import logging
import os

import boto3
from botocore.exceptions import ClientError

from python.src.models.User import User


class DynamoDbOperationUnsuccessfulError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class DynamoDbHelper:

    def __init__(self, client=None):
        if client is None:
            self.dynamodb_client = boto3.client('dynamodb', region_name=os.getenv('REGION', 'eu-west-1'))
        else:
            self.dynamodb_client = client

    def put_user(self, user: User, table_name: str = os.getenv('DYNAMODB_TABLE_NAME', 'Users')) -> None:
        try:
            dynamodb_put_item_response = self.dynamodb_client.put_item(
                TableName=table_name,
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

        except ClientError as boto_error:
            error_code = boto_error.response['Error']['Code']
            error_msg = boto_error.response['Error']['Message']
            if error_code == 'ResourceNotFoundException':
                logging.warning(f"Dynamodb table {table_name} not found")
            else:
                logging.warning(f"{error_code}:{error_msg}")
            raise boto_error
        except Exception as error:
            raise error

    def get_user(self, user: User, table_name: str = os.getenv('DYNAMODB_TABLE_NAME', 'Users')) -> User:
        try:
            dynamodb_get_item_response = self.dynamodb_client.get_item(
                TableName=table_name,
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

        except ClientError as boto_error:
            error_code = boto_error.response['Error']['Code']
            error_msg = boto_error.response['Error']['Message']
            if error_code == 'ResourceNotFoundException':
                logging.warning(f"Dynamodb table {table_name} not found")
            else:
                logging.warning(f"{error_code}:{error_msg}")

            raise boto_error
        except Exception as error:
            raise error
