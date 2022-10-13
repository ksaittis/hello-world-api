import json
import logging

from python.src.models.user import User
from python.src.utils.api_error_handling import handle_api_exceptions
from python.src.utils.dynamodb_helper import DynamoDbHelper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@handle_api_exceptions
def handler(event, context):
    logger.info(event)

    user = User.from_event(event)

    if not user.is_valid():
        logger.warning(f"User details not valid: {user}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }

    db_helper = DynamoDbHelper()
    db_helper.put_user(user)

    # If no exceptions were raised so far then operation was most likely successful
    return {
        'statusCode': 204,
        'body': ""
    }
