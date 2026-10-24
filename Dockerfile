FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto (incluindo a pasta tests/)
COPY . .

EXPOSE 8000

# O Render define a porta na variável PORT; localmente usa 8000.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
