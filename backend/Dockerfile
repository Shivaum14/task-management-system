FROM python:3.12-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_HOST=0.0.0.0 \
    APP_PORT=80

EXPOSE ${APP_PORT}

EXPOSE 80

ENTRYPOINT ["sh", "-c", "python -m app.main"]