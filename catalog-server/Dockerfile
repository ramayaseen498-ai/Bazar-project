FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY catalog.csv .
COPY catalog.py .

EXPOSE 5001

CMD ["python", "catalog.py"]
