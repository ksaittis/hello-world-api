import json
import logging

from python.src.models.User import User, EventParsingError
from python.src.utils.dynamodb_helper import DynamoDbHelper, DynamoDbOperationUnsuccessfulError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    try:
        user = User.from_event(event)

        if user.is_valid():
            db_helper = DynamoDbHelper()
            db_helper.put_user(user)

            # If no exceptions were raised so far then operation was most likely successful
            return {
                'statusCode': 204,
                'body': ""
            }

        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except (EventParsingError, DynamoDbOperationUnsuccessfulError, DynamoDbOperationUnsuccessfulError):
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error')
        }
