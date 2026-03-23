FROM python:3.12-slim

WORKDIR /app

# install uv
RUN pip install --no-cache-dir uv

# copy dependency files first
COPY pyproject.toml uv.lock ./

# install dependencies
RUN uv sync --no-dev

# copy app
COPY . .

# expose port
EXPOSE 8000

# run app
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["uv run uvicorn api.main:app --host 0.0.0.0 --port 8000"]