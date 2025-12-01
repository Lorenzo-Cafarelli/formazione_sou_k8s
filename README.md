# [Track 2] Jenkins & Ansible Ops + K8s Deploy & Quality Gate

Questo documento descrive in modo dettagliato l'intero ciclo di vita del progetto, suddiviso in 6 step operativi. Il progetto copre la configurazione dell'infrastruttura, la creazione di pipeline di build e deploy, e l'automazione delle verifiche su cluster Kubernetes.

---

## Step 1 - Workstation Mac

### Descrizione Esercizio
Lo scopo di questa fase è configurare un'architettura Jenkins distribuita composta da un nodo Master e un nodo Slave (Agent). Viene utilizzato Vagrant per la creazione della Macchina Virtuale e Ansible per l'orchestrazione e il deploy dei container. Il container Agent deve collegarsi al container Master per eseguire i task successivi.

### Tools Utilizzati
- Vagrant
- Ansible
- Jenkins

### Svolgimento Operativo
La procedura inizia con la configurazione del `Vagrantfile`, definendo una macchina virtuale basata su sistema operativo Rocky Linux 9. È fondamentale esporre le porte 8080 (per l'interfaccia web di Jenkins) e 50000 (per la comunicazione JNLP tra Master e Agent).

Successivamente, si interviene sul playbook Ansible per configurare la VM. Vengono installate le dipendenze necessarie quali Python, Java e Docker. Viene creato un Network Docker dedicato e vengono scaricate le immagini `jenkins/jenkins:lts` per il Master (denominato ContainerM) e `jenkins/inbound-agent` per lo Slave (denominato ContainerS). I container vengono avviati tramite il comando `vagrant up`.

Per completare l'installazione:
1. Si recupera la password iniziale di amministrazione eseguendo il comando `cat /var/jenkins_home/secrets/initialAdminPassword` all'interno del Container Master.
2. Si effettua il login all'indirizzo `http://localhost:8080`.
3. Si naviga nel percorso Dashboard/Nodi/ContainerS per ottenere il "secret" necessario alla connessione dell'agente.
4. Tale secret viene inserito nella configurazione del container Slave all'interno del playbook Ansible.
5. Si esegue `vagrant provision` per applicare le modifiche e finalizzare il collegamento tra i nodi.

---

## Step 2 - Pipeline Jenkins dichiarativa (Groovy) per build immagine Docker

### Descrizione Esercizio
L'obiettivo è creare un'applicazione Flask (Python) che esponga una pagina con la stringa "hello world" e realizzare un Dockerfile per la sua containerizzazione. Successivamente, si deve implementare una pipeline dichiarativa Jenkins che esegua la build dell'immagine e il push su DockerHub, applicando una logica di tagging condizionale basata sul ramo Git di provenienza.

### Tools Utilizzati
- Vagrant
- Ansible
- Jenkins
- Docker

### Svolgimento Operativo
Dopo aver creato lo script `app.py` e il relativo `Dockerfile`, si procede alla configurazione di Jenkins. Nella sezione "Credenziali" vengono salvate le credenziali di accesso per DockerHub e Git. La pipeline viene collegata alla repository remota per garantire l'esecuzione della versione più aggiornata del codice.

La pipeline esegue i seguenti passaggi:
1. **Checkout SCM**: Scarica il Jenkinsfile aggiornato dalla repository.
2. **Logica di Tagging**: Tramite una serie di condizioni "if", determina il tag dell'immagine:
   - Se la build è innescata da un tag Git, usa quel tag.
   - Se il ramo è `master`, usa il tag `latest`.
   - Se il ramo è `develop`, usa il tag formato da "develop" + SHA del commit.
   Il risultato viene salvato nella variabile `env.IMAGE_TAG`.
3. **Build & Push**: Esegue `docker build` utilizzando il tag calcolato e successivamente effettua il login e il push dell'immagine sul registro DockerHub.

---

## Step 3 - Helm Chart

### Descrizione Esercizio
In questa fase si richiede la creazione di un Helm Chart personalizzato per il deployment dell'applicazione creata nello step precedente. Il chart deve essere configurato per accettare in input il tag dell'immagine da rilasciare.

### Tools Utilizzati
- Helm Chart

### Svolgimento Operativo
Si utilizza il comando `helm init` (o `helm create` nelle versioni recenti) per generare la struttura base del chart. Sebbene la struttura venga creata in questo step, la configurazione dettagliata e la verifica del chart avvengono nello step successivo tramite l'integrazione nella pipeline di deployment.

---

## Step 4 - Helm Install

### Descrizione Esercizio
Lo scopo è scrivere una pipeline Jenkins che prelevi il chart versionato dalla repository Git ed esegua il comando `helm install` sull'istanza Kubernetes locale (Minikube) nel namespace `formazione-sou`.

### Tools Utilizzati
- Vagrant
- Ansible
- Jenkins
- Helm Chart

### Svolgimento Operativo
Sono necessarie configurazioni preliminari sul Container Slave (ContainerS) per permettere l'interazione con il cluster Host:
1. **Volumi Docker**: Nel playbook Ansible, vengono montati i volumi `/var/run/docker.sock:/var/run/docker.sock` (per comunicare con il daemon Docker dell'host) e `/usr/bin/docker:/usr/bin/docker`.
2. **Configurazione Kubernetes**: Si copiano il file `config` e i certificati (`Client.key`, `Client.crt`, `Ca.crt`) dalla macchina Host alla directory `/home/jenkins` del ContainerS. Il file `config` viene modificato (tramite editor Vim installato nel container) per puntare ai percorsi corretti dei certificati.

Lato Kubernetes, si avvia Minikube (`minikube start`) e si crea il namespace (`kubectl create namespace formazione-sou`). Si aggiorna il file `values.yaml` dell'Helm Chart inserendo l'immagine Docker creata nello Step 2.

La pipeline Jenkins esegue:
1. Clone della repository del chart.
2. Export della variabile `KUBECONFIG`.
3. Esecuzione di `helm upgrade --install` per rilasciare l'applicazione.
La verifica avviene controllando che il pod sia in stato "Running" e testando la risposta su `localhost:8000` tramite un container di test temporaneo.

---

## Step 5 - Check Deployment Best Practices

### Descrizione Esercizio
Si richiede lo sviluppo di uno script (Python) che, autenticandosi tramite un Service Account con permessi di lettura sul cluster, esporti il deployment dell'applicazione Flask. Lo script deve validare la presenza degli attributi: Readiness Probe, Liveness Probe, Limits e Requests.

### Tools Utilizzati
- Python (Librerie: client Kubernetes, config, ApiException)

### Svolgimento Operativo
Lo script importa le librerie client di Kubernetes per gestire l'autenticazione e le chiamate API.
Le funzioni principali implementate sono:
1. **authenticate_with_service_account**: Carica il `kubeconfig` e restituisce un oggetto API per interagire con i deployment.
2. **export_deployment_and_check**: Recupera il deployment specifico dal cluster e lo esporta in un file YAML locale.
3. **check_container_probes_and_resources**: Analizza la configurazione esportata verificando puntualmente la presenza delle sonde di monitoraggio (Readiness, Liveness) e dei vincoli sulle risorse (Limits, Requests). In caso di assenza di questi attributi, lo script restituisce un messaggio di errore.

---

## Step 6 - Bonus Track

### Descrizione Esercizio
L'ultimo step prevede l'implementazione di un Ingress Controller Nginx tramite Helm Chart. L'obiettivo è rendere l'applicazione raggiungibile via HTTP all'indirizzo `http://formazionesou.local`, restituendo la pagina "hello world".

### Tools Utilizzati
- Python (contesto generale)
- Kubernetes/Helm

### Svolgimento Operativo
Per esporre il servizio esternamente, si modifica il chart Helm:
1. Nel file `values.yaml` e `service.yaml`, il tipo di servizio viene cambiato da `ClusterIP` a `NodePort`, impostando la porta statica `31000`.
2. Si configura la risorsa Ingress specificando l'host `formazionesou.local`.

Dopo aver aggiornato il chart, si riesegue la pipeline Jenkins per applicare le modifiche. Sulla macchina locale è necessario:
1. Abilitare l'ingress controller su Minikube con il comando `minikube addons enable ingress`.
2. Modificare il file `/etc/hosts` aggiungendo l'associazione tra l'indirizzo IP di Minikube e il dominio `formazionesou.local`.

La verifica finale consiste nel navigare all'indirizzo `http://formazionesou.local` tramite browser, dove deve essere visualizzata correttamente la scritta "Helloworld".