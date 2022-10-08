import json
import logging
import os
from datetime import datetime, date
from typing import Optional

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_username_valid(username: str) -> bool:
    """
    Returns true if username contains only letters
    """
    if not isinstance(username, str) or not username.isalpha():
        return False
    return True


def is_birthday_today(date_of_birth: str) -> bool:
    """Returns true if day and month of date_of_birth matchs todays day and month"""
    try:
        date_of_birth_converted = datetime.strptime(date_of_birth, os.getenv('DATE_FORMAT', default='%Y-%m-%d'))
        today = date.today()
        return today.month == date_of_birth_converted.month and today.day == date_of_birth_converted.day
    except ValueError:
        raise False


def get_next_birthday(date_of_birth: str) -> Optional[date]:
    """Returns next birthday date"""
    try:
        date_of_birth_converted = datetime.strptime(date_of_birth, os.getenv('DATE_FORMAT', default='%Y-%m-%d')).date()
        today = date.today()

        if today.month > date_of_birth_converted.month or (
                date_of_birth_converted.month == today.month and today.day > date_of_birth_converted.day):
            return date_of_birth_converted.replace(year=today.year + 1)

        return date_of_birth_converted.replace(year=today.year)
    except ValueError:
        raise None


def get_days_until_next_birthday(date_of_birth: str) -> int:
    """Returns number of days until next birthday"""
    if is_birthday_today(date_of_birth):
        return 0

    next_birthday_date = get_next_birthday(date_of_birth)
    return (next_birthday_date - date.today()).days


def get_user(event, context):
    logger.info(event)

    try:
        username = event['pathParameters']['username']

        if is_username_valid(username):
            dynamodb_get_item_response = boto3.client('dynamodb').get_item(
                TableName=os.environ['DYNAMODB_TABLE_NAME'],
                Key={
                    'username': {
                        'S': username
                    }
                }
            )
            if dynamodb_get_item_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                date_of_birth = dynamodb_get_item_response['Item']['dateOfBirth']['S']
                if is_birthday_today(date_of_birth):
                    return {
                        'statusCode': 200,
                        'body': json.dumps(f"Hello {username}! Happy birthday!")
                    }

                days_until_next_birthday = get_days_until_next_birthday(date_of_birth)

                return {
                    'statusCode': 200,
                    'body': json.dumps(f"Hello {username}! Your birthday is in {days_until_next_birthday} day(s)!")
                }

    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error')
        }

    return {
        'statusCode': 400,
        'body': json.dumps(f'Bad Request')
    }


