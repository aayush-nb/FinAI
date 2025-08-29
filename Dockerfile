FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install system packages required for scientific/ML libs
# (adjust depending on your requirements.txt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first (important for wheels)
RUN pip install --upgrade pip wheel setuptools

# Copy only requirements first (leverage Docker cache)
COPY requirements.txt .

# Use BuildKit cache for pip (if enabled)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port (optional, for clarity)
EXPOSE 80

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
