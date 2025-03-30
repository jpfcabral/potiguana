resource "aws_lambda_function" "my_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repo.repository_url}:latest"
  package_type  = "Image"
  timeout       = 120
  memory_size   = 256
  environment {
    variables = {
      OPENAI_API_KEY       = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["openai_api_key"]
      VECTOR_STORE_URL     = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["vector_store_url"]
      VECTOR_STORE_API_KEY = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["vector_store_api_key"]
      TELEGRAM_API_TOKEN   = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["telegram_api_token"]
      LANGSMITH_TRACING    = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["langsmith_tracing"]
      LANGSMITH_ENDPOINT   = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["langsmith_endpoint"]
      LANGSMITH_API_KEY    = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["langsmith_api_key"]
      LANGSMITH_PROJECT    = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["langsmith_project"]
      MONGO_URI            = jsondecode(data.aws_secretsmanager_secret_version.my_secret_version.secret_string)["mongo_uri"]
    }
  }
}
