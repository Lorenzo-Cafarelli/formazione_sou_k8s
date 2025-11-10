pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        // Assicurati di avere questa credenziale su Jenkins se vuoi usare withKubeConfig
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
                    // Assicuriamoci che BRANCH_NAME abbia un valore, anche se di default
                    def currentBranch = env.BRANCH_NAME ?: 'unknown-branch'
                    
                    if (env.TAG_NAME) {
                        env.IMAGE_TAG = env.TAG_NAME
                    } else if (currentBranch == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else if (currentBranch == 'develop') {
                         // Gestiamo anche il caso in cui GIT_COMMIT potrebbe essere null
                         def commitHash = env.GIT_COMMIT ?: 'unknown-commit'
                         def shortCommit = commitHash.length() > 7 ? commitHash.substring(0, 7) : commitHash
                         env.IMAGE_TAG = "develop-${shortCommit}"
                    } else {
                        def safeBranchName = currentBranch.replaceAll('[^a-zA-Z0-9.-]', '_')
                        env.IMAGE_TAG = "${safeBranchName}-${env.BUILD_NUMBER}"
                    }
                    
                    echo "Git context: Branch=${currentBranch}, Tag=${env.TAG_NAME}"
                    echo "Docker image tag set to: ${env.IMAGE_TAG}"
                }
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh """
                        echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                        docker build -t ${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${IMAGE_TAG} .
                        docker push ${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${IMAGE_TAG}
                    """
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