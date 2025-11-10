pipeline {
    agent {
        // Impostiamo l'agente corretto che dovrebbe avere Podman
        label 'podman-agent-01'
    }

    environment {
        DOCKER_HUB_USER = 'lorenzocafarelli'
        IMAGE_NAME = "flask-app-example"
        // Se il tuo Dockerfile ha multi-stage e vuoi solo un target specifico,
        // decommenta la riga sotto e aggiungi '--target ${BUILD_TARGET}' al comando build
        // BUILD_TARGET = 'builder'
        DOCKERHUB_CRED_ID = 'dockerhub-creds'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Clono il codice su agent ..."
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    // Gestione più robusta del branch name se non è popolato automaticamente
                    def currentBranch = env.BRANCH_NAME ?: 'unknown'
                    if (currentBranch == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else {
                        env.IMAGE_TAG = "dev-${env.BUILD_NUMBER}"
                    }
                    echo "Podman image tag set to: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build Podman Image') {
            steps {
                echo "Buildo l'immagine ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} con Podman..."
                // Usa 'podman build'. Se serve il target, aggiungi: --target ${env.BUILD_TARGET}
                sh "podman build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKERHUB_CRED_ID,
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )]) {
                        echo "Logging into Docker Hub and pushing image with Podman..."

                        // Podman spesso richiede di specificare il registry per il login
                        sh "echo \$DOCKER_PASSWORD | podman login docker.io -u \$DOCKER_USERNAME --password-stdin"

                        // Push dell'immagine. Podman potrebbe richiedere il full path del registry.
                        // Se fallisce senza 'docker.io/', prova ad aggiungerlo:
                        // sh "podman push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} docker.io/${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                        sh "podman push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"

                        sh "podman logout docker.io"
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Cleaning up local image from agent...'
                // Usa 'podman rmi' per rimuovere l'immagine locale
                sh "podman rmi ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} || true" // || true evita che il fallimento del cleanup rompa la pipeline
            }
        }
    }
}