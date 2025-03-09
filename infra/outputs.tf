output "lambda_function_name" {
  description = "Deployed Lambda function name"
  value       = aws_lambda_function.my_lambda.function_name
}

output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.lambda_repo.repository_url
}

output "api_gateway_url" {
  value       = "${aws_apigatewayv2_api.lambda_api.api_endpoint}/potiguana"
  description = "A URL do endpoint do API Gateway"
}
