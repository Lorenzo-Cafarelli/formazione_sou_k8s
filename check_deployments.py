import yaml
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Configurazione Autenticazione
def authenticate():
    # Tenta prima di usare la configurazione locale (kubeconfig)
    # In uno scenario reale "in-cluster", si userebbe config.load_incluster_config()
    try:
        config.load_kube_config()
        print("Autenticato tramite Kubeconfig locale.")
    except Exception:
        print("Impossibile trovare kubeconfig. Tentativo in-cluster...")
        try:
            config.load_incluster_config()
            print("Autenticato tramite Service Account in-cluster.")
        except Exception as e:
            print(f"Errore di autenticazione: {e}")
            sys.exit(1)

    return client.AppsV1Api()

def check_requirements(deployment):
    """Controlla se il deployment ha i requisiti richiesti: Probe e Resources."""
    errors = []
    
    # Itera su tutti i container nel deployment
    for container in deployment.spec.template.spec.containers:
        name = container.name
        
        # 1. Controllo Readiness Probe
        if not container.readiness_probe:
            errors.append(f"Container '{name}': Manca Readiness Probe")
            
        # 2. Controllo Liveness Probe
        if not container.liveness_probe:
            errors.append(f"Container '{name}': Manca Liveness Probe")
            
        # 3. Controllo Resources (Limits e Requests)
        if not container.resources:
            errors.append(f"Container '{name}': Mancano definizioni Resources")
        else:
            # Verifica Limits
            if not container.resources.limits:
                errors.append(f"Container '{name}': Mancano Limits")
            # Verifica Requests
            if not container.resources.requests:
                errors.append(f"Container '{name}': Mancano Requests")

    return errors

def export_and_verify(deployment_name, namespace):
    api = authenticate()
    
    try:
        # Recupera il Deployment
        deployment = api.read_namespaced_deployment(deployment_name, namespace)
        print(f"Deployment '{deployment_name}' trovato nel namespace '{namespace}'.")

        # Esporta lo YAML su file (pulendo i metadati superflui)
        file_name = f"{deployment_name}_export.yaml"
        with open(file_name, 'w') as f:
            # Usiamo to_dict() per serializzare l'oggetto, poi puliamo con yaml dump
            # clean_deployment = api.api_client.sanitize_for_serialization(deployment)
            yaml.dump(deployment.to_dict(), f)
        print(f"Deployment esportato in: {file_name}")

        # Esegui i controlli
        errors = check_requirements(deployment)

        if errors:
            print("\n[ERRORE] Il deployment NON soddisfa i requisiti:")
            for err in errors:
                print(f" - {err}")
            # Usciamo con codice di errore per segnalare il fallimento alla CI/CD
            sys.exit(1) 
        else:
            print("\n[SUCCESSO] Il deployment soddisfa tutti i requisiti (Liveness, Readiness, Limits, Requests).")
            sys.exit(0)

    except ApiException as e:
        if e.status == 404:
            print(f"Errore: Deployment '{deployment_name}' non trovato nel namespace '{namespace}'.")
        else:
            print(f"Errore API Kubernetes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Configura qui i nomi corretti
    DEPLOYMENT_NAME = "my-flask-app"  # Nome del tuo deployment installato via Helm
    NAMESPACE = "formazione-sou"      # Namespace dell'esercizio
    
    export_and_verify(DEPLOYMENT_NAME, NAMESPACE)