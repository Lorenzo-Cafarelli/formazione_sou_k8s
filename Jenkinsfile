pipeline {
    agent {
        // Assicurati che il nuovo nodo che hai collegato a Jenkins abbia questa etichetta!
        label 'docker-agent'
    }

    environment {
        DOCKER_HUB_USER = 'lorenzocafarelli'
        IMAGE_NAME = "flask-app-example"
        // ID della credenziale salvata su Jenkins con username/password di Docker Hub
        DOCKERHUB_CRED_ID = 'dockerhub-creds'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Cloning repository on docker agent..."
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    def currentBranch = env.BRANCH_NAME ?: 'unknown'
                    if (currentBranch == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else {
                        env.IMAGE_TAG = "dev-${env.BUILD_NUMBER}"
                    }
                    echo "Docker image tag set to: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} with Docker..."
                // Usa 'docker build'
                sh "docker build -t ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
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
                        echo "Logging into Docker Hub..."
                        // Login standard Docker
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"

                        echo "Pushing image..."
                        sh "docker push ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"

                        sh "docker logout"
                    }
                }
            }
        }

	stage('Deploy to K8s') {
            steps {
                script {
                     // Assicurati di avere la credenziale 'k8s-kubeconfig' configurata su Jenkins!
                     withKubeConfig([credentialsId: 'k8s-kubeconfig']) {
                        echo "Deploying to Kubernetes with Helm..."
                        sh """
                            helm upgrade --install flask-app ./charts/flask-app-chart \
                              --namespace default \
                              --set image.repository=${env.DOCKER_HUB_USER}/${env.IMAGE_NAME} \
                              --set image.tag=${env.IMAGE_TAG} \
                              --wait
                        """
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Cleaning up local image...'
                // Pulizia con docker rmi
                sh "docker rmi ${env.DOCKER_HUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG} || true"
            }
        }
    }
}