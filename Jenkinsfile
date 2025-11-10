pipeline {
    agent any

    environment {
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
                    env.IMAGE_TAG = env.TAG_NAME ?: (currentBranch == 'main' ? 'latest' : "build-${env.BUILD_NUMBER}")
                    echo "Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build and Push') {
            agent {
                docker {
                    image 'docker:latest'
                    // Questo è fondamentale: monta il socket docker dell'host nel container
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
                    sh "docker build -t ${env.DOCKERHUB_CREDS_USR}/flask-app-example:${env.IMAGE_TAG} ."
                    sh "docker push ${env.DOCKERHUB_CREDS_USR}/flask-app-example:${env.IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to K8s') {
            // Assicurati che questo stage abbia i tool necessari (helm, kubectl)
            // Potresti dover usare un altro agent docker qui, es:
            // agent { docker { image 'dtzar/helm-kubectl:latest' } }
            steps {
                script {
                   // ... i tuoi comandi helm ...
                   echo "Simulazione deploy per ora"
                }
            }
        }
	stage('Debug Environment') {
            steps {
                  sh 'uname -a'
                  sh 'cat /etc/os-release'
                  sh 'find /usr -name podman 2>/dev/null || true'
                  sh 'find /usr -name buildah 2>/dev/null || true'
                  sh 'echo $PATH'
            }
        }
    }
}