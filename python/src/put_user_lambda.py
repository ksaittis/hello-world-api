import json
import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ParamValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_date_of_birth_valid(date_of_birth: str) -> bool:
    """
    Returns true if date_of_birth is valid datetime format and is before today
    """
    try:
        date_of_birth_converted = datetime.strptime(date_of_birth, os.getenv('DATE_FORMAT', default='%Y-%m-%d'))
        return date_of_birth_converted.date() < datetime.now().date()
    except ValueError:
        return False


def is_username_valid(username: str) -> bool:
    """
    Returns true if username contains only letters
    """
    if not isinstance(username, str) or not username.isalpha():
        return False
    return True


def put_user(event, context):
    logger.info(event)
    try:
        username = event['pathParameters']['username']
        date_of_birth = json.loads(event['body'])['dateOfBirth']

        if is_username_valid(username) and is_date_of_birth_valid(date_of_birth):
            dynamodb_put_item_response = boto3.client('dynamodb', region_name=os.environ['REGION']).put_item(
                TableName=os.environ['DYNAMODB_TABLE_NAME'],
                Item={
                    'username': {
                        'S': username
                    },
                    'dateOfBirth': {
                        'S': date_of_birth
                    }
                }
            )

            if 'HTTPStatusCode' in dynamodb_put_item_response and dynamodb_put_item_response['HTTPStatusCode'] == '200':
                return {
                    'statusCode': 204,
                    'body': ""
                }
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }

    except KeyError as key_error:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid request body, missing {key_error.args[0]}!')
        }
    except ParamValidationError:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad request, invalid param provided!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
