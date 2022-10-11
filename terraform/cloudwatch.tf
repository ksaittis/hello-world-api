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
  depends_on      = [aws_lambda_permission.allow_cloudwatch_invoke_monitoring_lambda]
}

resource "aws_cloudwatch_metric_alarm" "lambda_invocation" {
  alarm_name          = "${each.value}_lambda_invocation_alarm"
  alarm_description   = "This metric monitors the number of lambda invocations"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Invocations"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  unit                = "Count"
  threshold           = 10

  for_each = toset([
    aws_lambda_function.get_user.function_name,
    aws_lambda_function.put_user.function_name
  ])
  dimensions = {
    FunctionName = each.value
  }
  alarm_actions = [aws_sns_topic.lambda_failures.arn]
}
