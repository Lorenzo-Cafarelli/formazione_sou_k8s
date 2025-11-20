
## Step. 6
### Descrizione esercizio:

Lo scopo di questo esercizio è quello di equipaggiare l'istanza Kubernetes di un Ingress Controller Nginx, facendo in modo che l'Helm Chart installi anche l'ingress nginx.
Chiamando via HTTP http://formazionesou.local bisogna ottenere "hello world", ovvero quanto esposto dall'applicazione Flask creata nei punti precedenti.

### Tools utilizzati:
- Python (https://docs.python.org/3/)

### Svolgimento:

Dopo aver terminato lo step 4, andando sul Browser del computer locale su "http://localhost:8000" si poteva ricevere in output la stampa a video della scritta "Helloworld", il tutto dall' interno del Cluster.

Per avere lo stesso risultato fuori dal Cluster si può modificare il Chart: per prima cosa nel file Values.yaml si può modificare il service da ClusterIp (il quale permette solamente la comunicazione interna al Cluster) a NodePort (il quale mantiene una porta statica per la comunicazione esterna). Per configurare il NodePort è stata scelta la porta 31000, che è stata specificata nel file service.yaml. 

Tornando al file Values.yaml bisogna aggiungere un ingress che possa permettere la comunicazione con l'esterno. Bisogna aggiungere l' host "formazionesou.local", che sarà il sito su cui dovremo successivamente vedere la scritta "Helloworld".

Dopo aver terminato la modifica del Chart, per convenzione si può cancellare e ricreare il NameSpace "formazione-sou", per poi far partire nuovamente la Pipeline jenkins, andando ad installare il Chart modificato.

Poi si deve utilizzare il comando "minikube addons enable ingress" dal computer locale per abilitare il controller ingress.

Come ultimo step bisogna modificare il file /etc/hosts nel computer locale. Questo file funge da DNS, infatti si deve aggiungere l' ip di Minikube e l' indirizzo richiesto dalla traccia. In questo modo, per effettuare la verifica della riuscita dell' esercizio, si può navigare sul browser del nostro pc e chiamare la pagina http://formazionesou.local. Se lo step è stato effettuato correttamente, ci verrà restituita la scritta "Helloworld".
