resource "aws_cloudwatch_log_group" "get_user" {
  name              = "/aws/lambda/${aws_lambda_function.get_user.function_name}"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_group" "put_user" {
  name              = "/aws/lambda/${aws_lambda_function.put_user.function_name}"
  retention_in_days = 1
}

resource "aws_cloudwatch_log_group" "monitoring" {
  name              = "/aws/lambda/${aws_lambda_function.monitoring.function_name}"
  retention_in_days = 1
}


resource "aws_cloudwatch_log_subscription_filter" "failure_notification" {
  name     = "${aws_lambda_function.monitoring.function_name}_log_subscription"
  for_each = toset([
    aws_cloudwatch_log_group.get_user.name,
    aws_cloudwatch_log_group.put_user.name
  ])
  log_group_name = each.value

  filter_pattern  = "?ERROR ?CRITICAL ?5xx"
  destination_arn = aws_lambda_function.monitoring.arn
}
