ECR_REPOSITORY := potiguana-lambda-repo
IMAGE_TAG := latest
AWS_REGION := us-west-2
AWS_ACCOUNT_ID := $(shell aws sts get-caller-identity --query "Account" --output text)
TERRAFORM_DIR := ./infra
LAMBDA_FUNCTION_NAME := potiguana-bot-lambda

.PHONY: package requirements zip clean build push pull login-ecr deploy

# Default target
package: requirements install zip

# Generate requirements.txt from Pipenv
requirements:
	pipenv requirements > $(REQUIREMENTS_FILE)

# Install dependencies into the package directory
install:
	@rm -rf $(PACKAGE_DIR)
	mkdir -p $(PACKAGE_DIR)/python/lib/$(PYTHON_VERSION)/site-packages
	pip install -r $(REQUIREMENTS_FILE) -t $(PACKAGE_DIR)/python/lib/$(PYTHON_VERSION)/site-packages --upgrade

# Create a zip file of the package directory
zip:
	cd $(PACKAGE_DIR) && zip -r ../$(PACKAGE_ZIP) .

# Clean up generated files
clean:
	rm -rf $(PACKAGE_DIR) $(PACKAGE_ZIP) $(REQUIREMENTS_FILE)

# Build Docker image
build:
	docker build -t $(ECR_REPOSITORY) .

# Login to Amazon ECR
login-ecr:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

# Push Docker image to ECR
push: build login-ecr
	docker tag $(ECR_REPOSITORY):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG)
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG)

# Pull Docker image from ECR
pull: login-ecr
	docker pull $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG)

# Deploy using Terraform from ./infra
deploy: push pull
	cd $(TERRAFORM_DIR) && terraform init
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve -var-file="terraform.tfvars"
	aws lambda update-function-code \
		--function-name $(LAMBDA_FUNCTION_NAME) \
		--image-uri $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG) \
		--region $(AWS_REGION) > /dev/null
