
## Step. 4
### Descrizione esercizio:

Lo scopo di questo esercizio è quello di scrivere una pipeline dichiarativa Jenkins che prenda da GIT il repo chart versionato in "formazione_sou_k8s" ed effettui "helm install" sull'instanza K8s locale su namespace "formazione_sou".

### Tools utilizzati:
- Vagrant (https://developer.hashicorp.com/vagrant/docs)
- Ansible (https://docs.ansible.com/)
- Jenkins (https://www.jenkins.io/doc/)
- Helm Chart (https://helm.sh/docs/)

### Svolgimento:
Per svolgere questo step bisogna effettuare dei passaggi preliminari, per iniziare si deve installare Hypervisor su macchina host e modificare il playbook precedentemente configurato nello step 2, andando ad implementare Helm e Kubectl all' interno del container Slave. Bisogna modificare i "Volumes" del ContainerS, andando ad aggiungere il volume "/var/run/docker.sock:/var/run/docker.sock" e "/usr/bin/docker:/usr/bin/docker". Il primo volume consentirà di creare un "canale" che permetterà al ContainerS di comunicare direttamente con il daemon di Docker presente sull'host, il secondo permetterà di utilizzare "docker" presente sulla macchina Host all' interno di ContainerS.

Lato Kubernetes, per fare in modo che Container e macchina Host (su cui era già stato installato Minikube nello step 1) potessero comunicare, si deve effettuare la copia del File config dalla macchina Host al container Slave, nel percorso /.kube/config. 
Si deve poi effettuare anche la copia dei certificati Client.key, Client.crt e Ca.crt da Host a ContainerS nel percorso /home/jenkins. Bisogna poi modificare entrambi i file config, andando a specificare il percorso di questi certificati nell' apposito spazio.

Per effettuare questi due passaggi bisogna utilizzare l' editor "Vim", che bisogna installare (dopo aver fatto l' accesso alla CLI del ContainerS da Root User usando il comando sudo docker exec -it ContainerS /bin/bash) con il comando "apt-get install vim".

Sulla macchina host bisogna verificare che Minikube sia attivo utilizzando il comando "Minikube status", e nel caso non lo fosse si deve far partire con il comando "minikube start". Una volta partito, con il comando "kubectl create namespace formazione-sou" si può creare il namespace richiesto.

Poi si passa alla Pipeline Jenkins: bisogna creare un nuovo Jenkinsfile, in cui per prima cosa viene effettuato il "clone" della repository di GitHub in cui è contenuto il nostro Helm chart. Poi viene utilizzato il comando "export KUBECONFIG=/.kube/config" per exportare il file Config e il comando "helm upgrade --install" per far partire il nostro Helm Chart. 

Prima di far partire la Pipeline su Jenkins, si deve modificare il vero e proprio Helm Chart, avendolo lasciato "in sospeso" dallo step 3. All' interno bisogna specificare il namespace creato e si deve inserire l'immagine Docker creata nello step 2 come Container Image da utilizzare per la creazione del Pod.

Dopo aver fatto partire la Pipeline, si può verificare l' effettiva creazione del Pod usando il comando "kubectl get pod -n formazione-sou", verificando che sia nello stato "running".

Ultima verifica da poter effettuare è utilizzare il comando "docker run -p 8000:8000 giosuemanzo/flask-app-example:latest". Dopo aver creato questo container, dal browser del pc host dobbiamo navigare su "localhost:8000" (:8000 è la porta specificata nel Dockerfile dello step precedente). Così facendo viene stampata a video la scritta "Helloworld". 
