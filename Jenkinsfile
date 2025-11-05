pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Questo step popola automaticamente le variabili
                // env.BRANCH_NAME, env.TAG_NAME, env.GIT_COMMIT
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    if (env.TAG_NAME) {
                        // Caso 1: Build da tag Git
                        // env.TAG_NAME non è nullo, usiamo quello
                        env.IMAGE_TAG = env.TAG_NAME
                    } else if (env.BRANCH_NAME == 'main') {
                        // Caso 2: Build da branch master
                        env.IMAGE_TAG = 'latest'
                    } else if (env.BRANCH_NAME == 'develop') {
                        // Caso 3: Build da branch develop
                        // Usiamo i primi 7 caratteri dello SHA
                        env.IMAGE_TAG = "develop-${env.GIT_COMMIT.substring(0, 7)}"
                    } else {
                        // Fallback per altri branch (es. 'feature/login')
                        // Pulisce il nome (es. 'feature/login' -> 'feature_login')
                        def safeBranchName = env.BRANCH_NAME.replaceAll('[^a-zA-Z0-9.-]', '_')
                        env.IMAGE_TAG = "${safeBranchName}-${env.BUILD_NUMBER}"
                    }
                    
                    echo "Git context: Branch=${env.BRANCH_NAME}, Tag=${env.TAG_NAME}"
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
    }

    post {
        success {
            echo "Docker image pushed successfully!"
        }
        failure {
            echo "Pipeline failed. Check the logs."
        }
    }
}