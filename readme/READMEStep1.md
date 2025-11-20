
## Step. 1
### Descrizione esercizio:

Lo scopo di questo esercizio è quello di configurare un Jenkins Master e un Jenkins Slave, utilizzando Vagrant per creare la VM e Ansible per tirare su i 2 containers. Il container Agent si dovrà collegare al container Master per poter svolgere le operazioni descritte negli step successivi.

### Tools utilizzati:
- Vagrant (https://developer.hashicorp.com/vagrant/docs)
- Ansible (https://docs.ansible.com/)
- Jenkins (https://www.jenkins.io/doc/)

### Svolgimento:
Nel Vagrantfile creato va configurata la VirtualMachine (che chiameremo "macchina"), avente Rocky Linux 9 come sistema operativo. Devono essere configurate le porte 8080 e 50000, le quali serviranno successivamente.

Nel playbook bisogna andare a configurare la VirtualMachine: devono essere scaricati Python, Java, Docker e altre dipendenze, che serviranno per creare i 2 container richiesti per lo svolgimento dell' esercizio.

Difatti dopo la creazione di un Docker Network, dopo aver "pullato" l' immagine docker "jenkins/jenkins:lts" per il Master (ContainerM) e l' immagine docker jenkins/inbound-agent per l' Agent (ContainerS), si passa alla creazione dei containers.
Dopo aver utilizzato il comando "vagrant up" per tirare su Macchina Virtuale e containers, si può verificare la corretta creazione sfruttando il comando "ping". 

Si procede effettuando una connessione SSH sfruttando il comando "Vagrant SSH" sulla VM, per poi utilizzare il comando "sudo docker exec ContainerM cat /var/jenkins_home/secrets/initialAdminPassword". Grazie a questo comando si ricava la password di Login che servirà per entrare sul sito di Jenkins.

Dopo aver copiato la password, navigando sul browser del nostro pc Host, bisogna andare sulla pagina web di Jenkins all' indirizzo "http://localhost:8080". Dopo aver effettuato il login utilizzando come username "admin" e la suddetta password, bisogna seguire il percorso Dashboard/nodi/ContainerS per ricavare un'altra password, quella che permette il collegamento tra Jenkins Slave e Jenkins Master.

Dopo aver copiato quest' ultima password, bisogna intervenire sul playbook, andandola ad inserire nello spazio dedicato alla configurazione del Container Slave. 

Dopo aver salvato le nuove modifiche, si può utilizzare il comando "vagrant provision macchina" per fare in modo che le stesse vengano applicate e si possa effettuare il collegamento.

Infine, direttamente dall' interfaccia web di Jenkins, bisogna aggiungere il nodo "ContainerS" dal percorso Dashboard/Nodi/nuovo nodo. 
Dopo aver salvato le modifiche apportate, lo Slave sarà correttamente collegato al Master.
