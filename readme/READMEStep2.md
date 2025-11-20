
## Step. 2
### Descrizione esercizio:

Lo scopo di questo esercizio è quello di creare un Dockerfile app di esempio Flask (Python) che esponga una pagina avente stringa "hello world".
Successivamente dobbiamo scrivere una pipeline dichiarativa Jenkins che effettui una build dell'immagine Docker e che effettui il push sul proprio account DockerHub, avendo cura di inserire il tag git se "buildata" da tag git, latest se "buildata" da branch master e "develop + sha comit GIT" se "buildata" da branch develop.

### Tools utilizzati:
- Vagrant (https://developer.hashicorp.com/vagrant/docs)
- Ansible (https://docs.ansible.com/)
- Jenkins (https://www.jenkins.io/doc/)
- Docker (https://docs.docker.com/)

### Svolgimento:
Inizialmente si deve creare lo script Python all' interno del file "app.py" e poi si deve creare il Dockerfile richiesto.

Sulla pagina di Jenkins bisogna andare nella sezione "credenziali", per memorizzare le password del nostro account Dockerhub e del nostro account Git. 
Dalla sezione Dashboard/nome_pipeline/Configuration bisogna collegare la nostra Repository remota, selezionando le credenziali salvate in precedenza. In questo modo l' account Jenkins sarà direttamente collegato a quello Git, di conseguenza quando si proverà ad eseguire la Pipeline, verrà presa in considerazione quella presente sulla repository remota, piuttosto che quella presente sulla repository locale del nostro pc.

Dopo di ciò sul sito di Jenkins si possono scaricare i vari plugin che serviranno per eseguire la Pipeline, come quello di Git, Docker e altri ancora. 

La Pipeline è così strutturata: inizialmente viene effettuato un "Checkout scm", il quale permette di scaricare dalla Repository remota il Jenkinfile aggiornato, così da poter eseguire ogni volta la versione aggiornata con le ultime modifiche.

Successivamente sono stati creati una serie di "if", che permettono di verificare quale sia il tag corretto da inserire (come da indicazioni fornite). Il risultato di questa serie di "if" viene salvato nella variabile env.IMAGE_TAG.

Dopo viene effettuata la build dell' immagine utilizzando il comando "docker build -t", passando come parametro il registro Docker e la variabile env.IMAGE_TAG.

Infine viene effettuato il Login sul nostro account Dockerhub sfruttando le credenziali salvate in precedenza, e viene effettuato il Push dell' immagine.
