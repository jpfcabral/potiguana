FROM public.ecr.aws/lambda/python:3.11

# Define working directory inside the container
WORKDIR /var/task

# Copy Pipenv files first for dependency caching
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

# Copy application code
COPY ./src .

# Set the handler
CMD ["lambda_function.lambda_handler"]
