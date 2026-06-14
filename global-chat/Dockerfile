FROM python:3.14-slim
LABEL authors="wuff"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 12345
CMD ["python", "-u", "server.py"]