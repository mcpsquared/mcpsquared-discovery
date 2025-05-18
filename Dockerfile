# syntax=docker/dockerfile:1
# Dockerfile for building a Python image with Poetry
FROM python:3.12.7 as requirements-stage
WORKDIR /tmp
RUN pip install poetry==2.0.0
RUN pip install poetry-plugin-export==1.8.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12.7
WORKDIR /app

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

# Copy requirements and install dependencies
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application code and data
COPY . /app

# Ensure data directory exists and copy data files
RUN mkdir -p /app/src/mcpsquared_discovery/data
COPY src/mcpsquared_discovery/data/mcp_resources.md /app/src/mcpsquared_discovery/data/
COPY src/mcpsquared_discovery/data/mcp_servers.json /app/src/mcpsquared_discovery/data/

RUN pip install -e .

# Run the FastAPI application
CMD ["uvicorn", "mcpsquared_discovery.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "error"] 