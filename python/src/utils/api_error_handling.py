import json
import logging

from botocore.exceptions import ClientError

from python.src.models.user import EventParsingError
from python.src.utils.dynamodb_helper import DynamoDbOperationUnsuccessfulError, UserNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_api_exceptions(original_function):
    def decorated(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
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

    return decorated
