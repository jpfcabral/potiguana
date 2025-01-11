PACKAGE_DIR := package
PYTHON_VERSION := python3.11
REQUIREMENTS_FILE := requirements.txt
PACKAGE_ZIP := package.zip

.PHONY: package requirements zip clean

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
