import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def put_user(event, context):
    logger.info(event)
    try:
        username = event['pathParameters']['username']
        dateOfBirth = json.loads(event['body'])['dateOfBirth']

        return {
            'statusCode': 200,
            'body': json.dumps(f'User {username} injected successfully! {dateOfBirth}')
        }

    except KeyError as key_error:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid request body, missing {key_error.args[0]}!')
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Internal Server Error')
        }
