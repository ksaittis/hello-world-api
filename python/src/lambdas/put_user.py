import json
import logging
import os

from python.src.models.User import User, EventParsingError
from python.src.utils.dynamodb_helper import DynamoDbHelper, DynamoDbOperationUnsuccessfulError, DynamoDbError

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
    except (EventParsingError, DynamoDbOperationUnsuccessfulError, DynamoDbError):
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad Request')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error')
        }


if __name__ == '__main__':
    a = {
        "resource": "/hello/{username}",
        "path": "/hello/Hello",
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
            "username": "Hello"
        },
        "stageVariables": "None",
        "requestContext": {
            "resourceId": "di86x0",
            "resourcePath": "/hello/{username}",
            "httpMethod": "PUT",
            "extendedRequestId": "ZuxJxFU8joEFbRQ=",
            "requestTime": "09/Oct/2022:09:33:37 +0000",
            "path": "/v1/hello/Hello",
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
