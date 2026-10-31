FROM python:3.12-slim

WORKDIR /app

COPY programa.py .

CMD ["python", "programa.py"]