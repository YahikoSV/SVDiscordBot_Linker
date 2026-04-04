FROM python:3.14-slim

WORKDIR /app

RUN pip3 install -r requirements.txt && \
    playwright install chromium

COPY main.py .

CMD ["python3","main.py"]