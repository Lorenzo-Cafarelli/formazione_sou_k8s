
## Step. 5
### Descrizione esercizio:

Lo scopo di questo esercizio è quello di scrivere uno script Bash o Python che, autenticandosi tramite un Service Account di tipo "cluster-reader",  esegua un export del Deployment dell'applicazione Flask installata tramite lo Step 4. 
L'automatismo deve ritornare un errore se non presenti nel Deployment i seguenti attributi: Readiness, Liveness, Limits e Requests.

### Tools utilizzati:
- Python (https://docs.python.org/3/)

### Svolgimento:
Per prima cosa bisogna importare la libreria client, la quale contiene le API per interagire con Kubernetes (come l'API per i deployment, pod, ecc.), la libreria config, la quale permette di caricare e gestire la configurazione del kubeconfig e che contiene le credenziali per accedere al cluster Kubernetes, ed infine la libreria ApiException, per gestire le eccezioni durante le chiamate all'API di Kubernetes.

La funzione authenticate_with_service_account permette di autenticare l'utente al cluster Kubernetes.
Se viene passato un percorso del file kubeconfig (kubeconfig_path), viene caricato quel file. Altrimenti, carica il kubeconfig predefinito.
Dopo aver caricato la configurazione, restituisce un oggetto AppsV1Api, che consente di interagire con i deployment.

La funzione check_container_probes_and_resources verifica la presenza di Readiness, Liveness, Limits e Requests nella configurazione, come richiesto dalla traccia.

La funzione export_deployment_and_check per prima cosa autentica l'utente andando a richiamare la funzione apposita, recupera un deployment specifico dal cluster Kubernetes e lo esporta in un file YAML ({deployment_name}_deployment.yaml).

Successivamente viene chiamata la funzione check_container_probes_and_resources per effettuare le varie verifiche e ne vengono stampati i risultati. Qualora ci fossero errori durante l' esportazione del deployment, verrà stampato un messaggio di avviso.
