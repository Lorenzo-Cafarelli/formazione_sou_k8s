# --- STAGE 1: Costruzione ---

# 1. Immagine di base: usa un'immagine Python ufficiale e leggera
FROM python:3.11-slim-buster

# 2. Imposta la directory di lavoro nel container
WORKDIR /app

# 3. Crea un utente non-root per motivi di sicurezza
# Crea un gruppo e un utente 'appuser' con ID 5001
RUN adduser -u 5001 --disabled-password --gecos "" appuser

# 4. Installa le dipendenze
# Copia prima il file requirements.txt per sfruttare la cache di Docker
COPY requirements.txt requirements.txt
# Installa le dipendenze senza salvare la cache di pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia il codice dell'applicazione
# Assegna la proprietà dei file all'utente 'appuser'
COPY --chown=appuser:appuser . .

# 6. Imposta l'utente per eseguire l'applicazione
USER appuser

# 7. Esponi la porta su cui gira l'app (definita in app.py)
EXPOSE 5000

# 8. Definisci il comando per avviare l'applicazione
CMD ["python", "app.py"]
