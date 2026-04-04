FROM python:3.14-slim

WORKDIR /app

COPY . ./

RUN pip3 install -r requirements.txt && \
    playwright install --with-deps chromium



CMD ["python3","main.py"]
