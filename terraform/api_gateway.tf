data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

resource "aws_api_gateway_rest_api" "hello_world" {
  name = var.rest_api_name

  endpoint_configuration {
    types = [
      "REGIONAL"
    ]
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_api_gateway_resource" "hello" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  parent_id = aws_api_gateway_rest_api.hello_world.root_resource_id
  path_part = "hello"
}

resource "aws_api_gateway_resource" "username_path_param" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  parent_id = aws_api_gateway_resource.hello.id
  path_part = "{username}"
}

resource "aws_api_gateway_method" "get_user" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  resource_id = aws_api_gateway_resource.username_path_param.id
  http_method = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.username" = true
  }
}

resource "aws_api_gateway_method" "put_user" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  resource_id = aws_api_gateway_resource.username_path_param.id
  http_method = "PUT"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.username" = true
  }
}

resource "aws_api_gateway_integration" "get_user" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  resource_id = aws_api_gateway_resource.username_path_param.id
  http_method = aws_api_gateway_method.get_user.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.get_user.invoke_arn
}

resource "aws_api_gateway_integration" "put_user" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  resource_id = aws_api_gateway_resource.username_path_param.id
  http_method = aws_api_gateway_method.put_user.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.put_user.invoke_arn
}

resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  resource_id = aws_api_gateway_resource.username_path_param.id
  http_method = aws_api_gateway_method.get_user.http_method
  status_code = "200"
}

resource "aws_api_gateway_deployment" "v1" {
  rest_api_id = aws_api_gateway_rest_api.hello_world.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.hello_world.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "v1" {
  deployment_id = aws_api_gateway_deployment.v1.id
  rest_api_id = aws_api_gateway_rest_api.hello_world.id
  stage_name = "v1"
}

output "invoke_url" {
  value = aws_api_gateway_stage.v1.invoke_url
}
