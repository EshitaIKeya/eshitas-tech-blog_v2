FROM python:3.13-slim

WORKDIR /app

# Build tools as a safety net — most packages install from prebuilt wheels,
# but if pip ever needs to compile one from source (e.g. on an unusual
# platform), these let it succeed instead of failing with a missing pg_config.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
