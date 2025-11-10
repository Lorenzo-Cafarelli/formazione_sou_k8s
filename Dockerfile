# Usa l'immagine ufficiale dell'agente Jenkins come base
FROM jenkins/inbound-agent:latest

# Passa all'utente root per installare i pacchetti
USER root

# Aggiorna i repository e installa dipendenze di base
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Aggiungi la chiave GPG ufficiale di Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Imposta il repository stabile di Docker
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installa il Docker CLI (solo il client, non il demone)
RUN apt-get update && \
    apt-get install -y docker-ce-cli

# (Opzionale ma consigliato) Installa anche Helm e Kubectl per lo stage di deploy
# Installa kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Installa Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Torna all'utente jenkins per sicurezza
USER jenkins