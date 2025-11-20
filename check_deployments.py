from kubernetes import client, config
from kubernetes.client.rest import ApiException

def authenticate_with_service_account(kubeconfig_path=None):
    if kubeconfig_path:
        config.load_kube_config(config_file=kubeconfig_path)
    else:
        config.load_kube_config()

    return client.AppsV1Api()  

def check_container_probes_and_resources(deployment):
    results = {"readinessProbe": [], "livenessProbe": [], "resources": []}

    for container in deployment.spec.template.spec.containers:
        container_name = container.name

        if container.readiness_probe:
            results["readinessProbe"].append((container_name, True))
        else:
            results["readinessProbe"].append((container_name, False))

        if container.liveness_probe:
            results["livenessProbe"].append((container_name, True))
        else:
            results["livenessProbe"].append((container_name, False))

        if container.resources:
            resources = container.resources
            has_limits = "limits" in resources
            has_requests = "requests" in resources
            results["resources"].append((container_name, has_limits, has_requests))
        else:
            results["resources"].append((container_name, False, False))

    return results

def export_deployment_and_check(deployment_name, namespace="formazione-sou"):
    try:
        apps_v1 = authenticate_with_service_account(kubeconfig_path="path_to_your_kubeconfig.yaml")
        
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        
        print(f"Deployment '{deployment_name}' esportato con successo!")
        with open(f"{deployment_name}_deployment.yaml", "w") as file:
            yaml.dump(deployment.to_dict(), file)

        results = check_container_probes_and_resources(deployment)
        
        print("\nVerifica dei container:")
        for probe_type, containers in results.items():
            for container_name, result in containers:
                if probe_type == "resources":
                    has_limits, has_requests = result
                    print(f"Container '{container_name}': Risorse - limits: {has_limits}, requests: {has_requests}")
                else:
                    print(f"Container '{container_name}': {probe_type} presente: {result}")

    except ApiException as e:
        print(f"Errore durante l'esportazione del deployment: {e}")

if __name__ == "__main__":
    export_deployment_and_check("flask-app-deployment", namespace="formazione-sou")
