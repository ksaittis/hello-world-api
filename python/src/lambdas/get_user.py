import json
import logging

from botocore.exceptions import ClientError

from python.src.models.user import User, EventParsingError
from python.src.utils.dynamodb_helper import DynamoDbHelper, DynamoDbOperationUnsuccessfulError, UserNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(event)

    try:
        user = User.from_event(event)

        if not user.is_username_valid():
            logger.warning(f"Username not valid format: {user.username.value}")
            return {
                'statusCode': 400,
                'body': json.dumps(f'Bad Request')
            }

        db_helper = DynamoDbHelper()
        user = db_helper.get_user(user)

        return {
            'statusCode': 200,
            'body': json.dumps({"message": user.get_greeting()})
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
