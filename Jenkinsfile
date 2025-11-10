pipeline {
    agent any // Oppure configura un agente specifico se sai quale ha docker

    environment {
        // Usa credentials() per gestire meglio le password ed evitare il warning di sicurezza
        DOCKERHUB_CREDS = credentials('dockerhub-creds') 
        // KUBECONFIG_CREDENTIAL_ID = 'k8s-kubeconfig' 
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    def currentBranch = env.BRANCH_NAME ?: 'unknown'
                    if (env.TAG_NAME) {
                        env.IMAGE_TAG = env.TAG_NAME
                    } else if (currentBranch == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else {
                        // Fallback generico
                        env.IMAGE_TAG = "build-${env.BUILD_NUMBER}"
                    }
                    echo "Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Usa le variabili d'ambiente per il login (più sicuro)
                    sh 'echo $DOCKERHUB_CREDS_PSW | podman login docker.io -u $DOCKERHUB_CREDS_USR --password-stdin'
                    
                    // Costruisci l'immagine
                    sh "podman build -t ${env.DOCKERHUB_CREDS_USR}/flask-app-example:${env.IMAGE_TAG} ."
                    
                    // Fai il push (potrebbe essere necessario specificare docker.io)
                    sh "podman push ${env.DOCKERHUB_CREDS_USR}/flask-app-example:${env.IMAGE_TAG} docker.io/${env.DOCKERHUB_CREDS_USR}/flask-app-example:${env.IMAGE_TAG}"
                }
            }
        }
        stage('Deploy to K8s') {
            steps {
                script {
                    // Assicurati che il plugin 'Kubernetes CLI' sia installato su Jenkins per usare 'withKubeConfig'
                    // Se non usi il plugin, devi assicurarti che 'kubectl' e 'helm' siano configurati sull'agente.
                    withKubeConfig([credentialsId: 'k8s-kubeconfig']) {
                        sh """
                            helm upgrade --install flask-app ./formazione_sou_k8s/charts/flask-app-example \
                              --namespace default \
                              --create-namespace \
                              --set image.repository=${DOCKERHUB_CREDENTIALS_USR}/flask-app-example \
                              --set image.tag=${IMAGE_TAG} \
                              --wait
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check the logs."
        }
    }
}