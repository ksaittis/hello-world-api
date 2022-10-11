variable "rest_api_name" {
  type = string
  default = "hello-world"
}

variable "lambdas_dir" {
  type = string
  default = "package"
}

variable "lambda_filename" {
  type = string
  default = "hello-world.zip"
}

variable "project_name" {
  type = string
  default = "hello-world"
}

variable "dynamodb_table_name" {
  type = string
  default = "Users"
}

variable "lambda_failure_notify_email" {
  type = string
  default = "ksaittis@gmail.com"
}
