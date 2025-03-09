data "aws_secretsmanager_secret" "my_secret" {
  name = var.secretsmanager_name
}

data "aws_secretsmanager_secret_version" "my_secret_version" {
  secret_id = data.aws_secretsmanager_secret.my_secret.id
}
