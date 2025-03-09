#trivy:ignore:AVD-AWS-0031
resource "aws_ecr_repository" "lambda_repo" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
