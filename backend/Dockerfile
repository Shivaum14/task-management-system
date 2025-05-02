## ------------------------------- Builder Stage ------------------------------ ## 
FROM python:3.12-slim AS builder

#  PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files to disk
#  PYTHONUNBUFFERED=1 ensures that Python output is sent straight to terminal (e.g. for logs)
#  PIP_NO_CACHE_DIR=1 disables the cache for pip, which can save space in the image
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 

WORKDIR /app

# --no-cache-dir prevents pip from caching the packages, which can save space in the image
# rm -rf /var/lib/apt/lists/* clears out package lists and caches to shrink the layer size.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# downloads (pre-)builds wheel files for every requirement into /wheels rather than installing them.
# wheel files are a binary distribution format for Python packages, which makes installation faster as they
# contain already-built pure-Python files and/or compiled extension modules as opposed to raw source code.
# This is useful for creating a layer with all dependencies pre-built, which can be reused in the runtime stage.
RUN pip install --upgrade pip --no-cache-dir \
    && pip wheel --wheel-dir=/wheels --no-cache-dir -r requirements.txt

## ------------------------------- Runtime Stage ------------------------------ ##
FROM python:3.12-slim AS runtime

ENV APP_HOST=0.0.0.0 \
    APP_PORT=80 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /app

# Brings in the pre-built wheel files from the builder stage.
COPY --from=builder /wheels /wheels

# installs every wheel into /usr/local, your default Python install area.
RUN pip install --prefix=/usr/local /wheels/* --no-cache-dir \
    && rm -rf /wheels

COPY ./app app

EXPOSE ${APP_PORT}

CMD ["python", "-m", "app.main"]
