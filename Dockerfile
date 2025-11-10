# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia i file dei requisiti (se ne hai, altrimenti puoi saltare questa riga o crearne uno vuoto)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Installa Flask direttamente (se non hai un requirements.txt)
RUN pip install flask

# Copia tutto il resto del codice sorgente nel container
COPY . .

# Esponi la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione.
# Usa python app.py per sfruttare il blocco `if __name__ == '__main__':` che hai configurato correttamente.
CMD ["python", "app.py"]