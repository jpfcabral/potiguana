variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "potiguana-bot-lambda"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "potiguana-lambda-repo"
}

variable "api_gateway_name" {
  description = "Name of the API Gateway"
  type        = string
  default     = "potiguana-gateway"
}

variable "secretsmanager_name" {
  description = "Name of the Secrets Manager secret"
  type        = string
  default     = "dev/potiguana"
}
