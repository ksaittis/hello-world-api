import json
import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ParamValidationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_date_of_birth_valid(date_of_birth: str) -> bool:
    """
    Returns true if date_of_birth is valid datetime format and is before today
    """
    try:
        date_of_birth_converted = datetime.strptime(date_of_birth, os.getenv('DATE_FORMAT', default='%Y-%m-%d'))
        return date_of_birth_converted.date() < datetime.now().date()
    except ValueError:
        return False


def is_username_valid(username: str) -> bool:
    """
    Returns true if username contains only letters
    """
    if not isinstance(username, str) or not username.isalpha():
        return False
    return True


def put_user(event, context):
    logger.info(event)
    try:
        username = event['pathParameters']['username']
        date_of_birth = json.loads(event['body'])['dateOfBirth']

        if is_username_valid(username) and is_date_of_birth_valid(date_of_birth):
            dynamodb_put_item_response = boto3.client('dynamodb', region_name=os.environ['REGION']).put_item(
                TableName=os.environ['DYNAMODB_TABLE_NAME'],
                Item={
                    'username': {
                        'S': username
                    },
                    'dateOfBirth': {
                        'S': date_of_birth
                    }
                }
            )

            if dynamodb_put_item_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'statusCode': 204,
                    'body': ""
                }
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request!')
        }

    except KeyError as key_error:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid request body, missing {key_error.args[0]}!')
        }
    except ParamValidationError:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad request, invalid param provided!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }


if __name__ == '__main__':
    a = {
        "resource": "/hello/{username}",
        "path": "/hello/giannis",
        "httpMethod": "PUT",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Content-Type": "text/plain",
            "Host": "8x16jn9bu7.execute-api.eu-west-1.amazonaws.com",
            "Postman-Token": "a43d67d7-4615-4af0-9983-b7e0a1ac9dd7",
            "User-Agent": "PostmanRuntime/7.29.2",
            "X-Amzn-Trace-Id": "Root=1-63429571-64b78dd6357341ea6ba4255c",
            "X-Forwarded-For": "54.86.50.139",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate, br"],
            "Cache-Control": ["no-cache"],
            "Content-Type": ["text/plain"],
            "Host": ["8x16jn9bu7.execute-api.eu-west-1.amazonaws.com"],
            "Postman-Token": ["a43d67d7-4615-4af0-9983-b7e0a1ac9dd7"],
            "User-Agent": ["PostmanRuntime/7.29.2"],
            "X-Amzn-Trace-Id": ["Root=1-63429571-64b78dd6357341ea6ba4255c"],
            "X-Forwarded-For": ["54.86.50.139"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"]
        },
        "queryStringParameters": "None",
        "multiValueQueryStringParameters": "None",
        "pathParameters": {
            "username": "giannis"
        },
        "stageVariables": "None",
        "requestContext": {
            "resourceId": "di86x0",
            "resourcePath": "/hello/{username}",
            "httpMethod": "PUT",
            "extendedRequestId": "ZuxJxFU8joEFbRQ=",
            "requestTime": "09/Oct/2022:09:33:37 +0000",
            "path": "/v1/hello/giannis",
            "accountId": "208867598194",
            "protocol": "HTTP/1.1",
            "stage": "v1",
            "domainPrefix": "8x16jn9bu7",
            "requestTimeEpoch": 1665308017541,
            "requestId": "fc5c0e4f-01d3-4dd2-80b5-e042236da4d5",
            "identity": {
                "cognitoIdentityPoolId": "None",
                "accountId": "None",
                "cognitoIdentityId": "None",
                "caller": "None",
                "sourceIp": "54.86.50.139",
                "principalOrgId": "None",
                "accessKey": "None",
                "cognitoAuthenticationType": "None",
                "cognitoAuthenticationProvider": "None",
                "userArn": "None",
                "userAgent": "PostmanRuntime/7.29.2",
                "user": "None"
            },
            "domainName": "8x16jn9bu7.execute-api.eu-west-1.amazonaws.com",
            "apiId": "8x16jn9bu7"
        },
        "body": "{\n    \"dateOfBirth\" : \"2020-08-01\"\n}",
        "isBase64Encoded": "False"
    }
    os.environ["REGION"] = "eu-west-1"
    os.environ["DYNAMODB_TABLE_NAME"] = "Users"
    os.environ['AWS_PROFILE'] = 'development'

    put_user(a, None)
