resource "aws_dynamodb_table" "users" {
  name = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "username"

  attribute {
    name = "username"
    type = "S"
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role_policy" "modify_dynamodb" {
  name = "lambda_modify_dynamodb_policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Effect = "Allow"
        Resource = aws_dynamodb_table.users.arn
      },
    ]
  })
}
