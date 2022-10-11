locals {
  allow_lambda_to_assume_role = {
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Sid       = ""
        Principal = {
          "Service" : "lambda.amazonaws.com"
        }
      },
    ]
  }
}
resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.api_lambda.name
  policy_arn = aws_iam_policy.cloudwatch_logging.arn
}

resource "aws_iam_role" "api_lambda" {
  name = "${var.project_name}-api-lambda-role"

  assume_role_policy = jsonencode(local.allow_lambda_to_assume_role)

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role" "monitoring_lambda" {
  name = "${var.project_name}-monitoring-lambda-role"

  assume_role_policy = jsonencode(local.allow_lambda_to_assume_role)

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "monitoring_cloudwatch_logging" {
  role = aws_iam_role.monitoring_lambda.name
  policy_arn = aws_iam_policy.cloudwatch_logging.arn
}

resource "aws_iam_role_policy_attachment" "monitoring_publish_sns" {
  role = aws_iam_role.monitoring_lambda.name
  policy_arn = aws_iam_policy.publish_to_topic.arn
}

resource "aws_iam_policy" "cloudwatch_logging" {
  name        = "cloudwatch_logging"
  path        = "/"
  description = "IAM policy for creating logs into cloudwatch"

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


resource "aws_iam_policy" "publish_to_topic" {
  name        = "publish_to_${aws_sns_topic.lambda_failures.name}_topic"
  path        = "/"
  description = "IAM policy for publishing a message to a topic"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Effect": "Allow",
        "Action": "sns:Publish",
        "Resource": "${aws_sns_topic.lambda_failures.arn}"
    }
  ]
}
EOF

  tags = {
    Project = var.project_name
  }
}
