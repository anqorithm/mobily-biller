# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Copy source code
COPY src/ ./src/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "fastapi", "run", "src/api/main.py", "--host", "0.0.0.0"] 