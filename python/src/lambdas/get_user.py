import json
import logging

from python.src.models.User import User, EventParsingError
from python.src.utils.dynamodb_helper import DynamoDbHelper, DynamoDbOperationUnsuccessfulError, UserNotFoundError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    try:
        user = User.from_event(event)

        if user.is_username_valid():
            db_helper = DynamoDbHelper()
            user = db_helper.get_user(user)

            return {
                'statusCode': 200,
                'body': json.dumps({"message": user.get_greeting()})
            }

        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except (EventParsingError, DynamoDbOperationUnsuccessfulError,
            DynamoDbOperationUnsuccessfulError, UserNotFoundError):
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error')
        }
