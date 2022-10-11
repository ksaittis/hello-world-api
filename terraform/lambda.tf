locals {
  lambda_filepath = "../${path.module}/${var.lambdas_dir}/${var.lambda_filename}"
  lambda_env_vars = {
    DYNAMODB_TABLE_NAME = aws_dynamodb_table.users.name
    REGION              = data.aws_region.current.name
    DATE_FORMAT         = "%Y-%m-%d"
  }
}

resource "aws_lambda_function" "get_user" {
  function_name = "get-user"
  filename      = local.lambda_filepath
  role          = aws_iam_role.api_lambda.arn
  handler       = "python.src.lambdas.get_user.handler"
  runtime       = "python3.9"

  source_code_hash = filebase64sha256(local.lambda_filepath)

  environment {
    variables = local.lambda_env_vars
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_lambda_function" "put_user" {
  function_name = "put-user"
  filename      = local.lambda_filepath
  role          = aws_iam_role.api_lambda.arn
  handler       = "python.src.lambdas.put_user.handler"
  runtime       = "python3.9"

  source_code_hash = filebase64sha256(local.lambda_filepath)

  environment {
    variables = local.lambda_env_vars
  }

  tags = {
    Project = var.project_name
  }
}


resource "aws_lambda_permission" "get_user_apigw_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_user.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.hello_world.id}/*/${aws_api_gateway_method.get_user.http_method}${aws_api_gateway_resource.hello.path}/*"
}

resource "aws_lambda_permission" "put_user_apigw_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.put_user.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.hello_world.id}/*/${aws_api_gateway_method.put_user.http_method}${aws_api_gateway_resource.hello.path}/*"
}

# Monitoring Lambda
resource "aws_lambda_permission" "allow_cloudwatch_invoke_monitoring_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monitoring.arn
  principal     = "logs.${data.aws_region.current.name}.amazonaws.com"

  for_each = toset([
    aws_cloudwatch_log_group.get_user.arn,
    aws_cloudwatch_log_group.put_user.arn
  ])

  source_arn = each.value
}

#resource "aws_lambda_permission" "allow_cloudwatch_invoke_monitoring_lambda" {
#  action        = "lambda:InvokeFunction"
#  function_name = aws_lambda_function.monitoring.arn
#  principal     = "logs.${data.aws_region.current.name}.amazonaws.com"
#  source_arn    = aws_cloudwatch_log_group.get_user.arn
#}

resource "aws_lambda_function" "monitoring" {
  function_name = "notify_on_error"
  filename      = local.lambda_filepath
  role          = aws_iam_role.api_lambda.arn
  handler       = "python.src.lambdas.notify_on_error.handler"
  runtime       = "python3.9"

  source_code_hash = filebase64sha256(local.lambda_filepath)

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.lambda_failures.arn
    }
  }

  tags = {
    Project = var.project_name
  }
}
