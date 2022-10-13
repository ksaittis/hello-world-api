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
