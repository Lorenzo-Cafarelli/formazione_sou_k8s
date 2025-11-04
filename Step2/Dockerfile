# 1. Definizione ambiente operativo Python
FROM python:3.11-alpine

# 2. iImposta directory di lavoro nel container
WORKDIR /app

# 3. Installazione delle dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia del codice
COPY app.py .

# 5. Porta esposta
EXPOSE 8080

# 6. Comando di avvio del container
CMD ["python", "app.py"]
