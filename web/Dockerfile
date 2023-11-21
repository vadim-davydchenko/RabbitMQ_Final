FROM python:3.9.18-alpine3.18
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
