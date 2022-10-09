resource "aws_lambda_function" "get_user" {
  function_name = "get-user"
  filename = "../${path.module}/${var.lambdas_dir}/get_user_lambda.zip"
  role = aws_iam_role.lambda.arn
  handler = "get_user_lambda.get_user"
  runtime = "python3.9"

  source_code_hash = filebase64sha256("../${path.module}/${var.lambdas_dir}/get_user_lambda.zip")

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.users.name
      REGION = data.aws_region.current.name
      DATE_FORMAT = "%Y-%m-%d"
    }
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_lambda_function" "put_user" {
  function_name = "put-user"
  filename = "../${path.module}/${var.lambdas_dir}/put_user_lambda.zip"
  role = aws_iam_role.lambda.arn
  handler = "put_user_lambda.put_user"
  runtime = "python3.9"

  source_code_hash = filebase64sha256("../${path.module}/${var.lambdas_dir}/put_user_lambda.zip")

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.users.name
      REGION = data.aws_region.current.name
      DATE_FORMAT = "%Y-%m-%d"
    }
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_cloudwatch_log_group" "get_user" {
  name              = "/aws/lambda/${aws_lambda_function.get_user.function_name}"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_group" "put_user" {
  name              = "/aws/lambda/${aws_lambda_function.put_user.function_name}"
  retention_in_days = 1
}

resource "aws_iam_policy" "lambda_cloudwatch_logging" {
  name        = "lambda_cloudwatch_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_cloudwatch_logging.arn
}

resource "aws_iam_role" "lambda" {
  name = "hello-world-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid = ""
        Principal = {
          "Service": "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Project = var.project_name
  }
}

resource "aws_lambda_permission" "get_user_apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_user.function_name
  principal = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.hello_world.id}/*/${aws_api_gateway_method.get_user.http_method}${aws_api_gateway_resource.hello.path}/*"
}

resource "aws_lambda_permission" "put_user_apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.put_user.function_name
  principal = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.hello_world.id}/*/${aws_api_gateway_method.put_user.http_method}${aws_api_gateway_resource.hello.path}/*"
}
