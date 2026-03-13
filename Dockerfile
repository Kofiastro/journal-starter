FROM python:3.12-slim

WORKDIR /app

# install uv
RUN pip install --no-cache-dir uv

# copy dependency files first (for Docker caching)
COPY pyproject.toml uv.lock ./

# install dependencies
RUN uv sync --no-dev

# copy the rest of the project
COPY . .

# run the app
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]