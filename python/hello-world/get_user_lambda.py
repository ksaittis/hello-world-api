import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_user(event, context):
    logger.info(event)

    try:
        username = event['pathParameters']['username']
        return {
            'statusCode': 200,
            'body': json.dumps(f'Hello {username}!')
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Unable to parse username!')
        }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error')
        }


