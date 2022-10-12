import json
import logging

from botocore.exceptions import ClientError

from python.src.models.user import User, EventParsingError
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
    except (EventParsingError, DynamoDbOperationUnsuccessfulError, UserNotFoundError):
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }

    except ClientError as error:
        logging.error(
            f"Boto client error: {error.response['Error']['Code']}, message: {error.response['Error']['Message']}")
    except Exception as e:
        logging.error(f"Internal server error, {e}")

    return {
        'statusCode': 500,
        'body': json.dumps(f'Internal server error')
    }
