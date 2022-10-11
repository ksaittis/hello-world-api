resource "aws_sns_topic" "lambda_failures" {
  name = "lambda-failures-topic"

  tags = {
    Project = var.project_name
  }
}

resource "aws_sns_topic_subscription" "lambda_failures" {
  topic_arn = aws_sns_topic.lambda_failures.arn
  protocol  = "email"
  endpoint  = var.lambda_failure_notify_email
}
