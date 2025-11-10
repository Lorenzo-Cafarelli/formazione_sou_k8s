pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
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
                    if (env.BRANCH_NAME == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else {
                        env.IMAGE_TAG = "dev-${env.BUILD_NUMBER}"
                    }
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