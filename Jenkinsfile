pipeline {
    agent any

    stages {
        stage('Debug Info') {
            steps {
                script {
                    echo "=== System Info ==="
                    sh 'uname -a'
                    sh 'cat /etc/os-release'
                    echo "=== Checking for Container Tools ==="
                    // Usa 'command -v' per vedere se i comandi esistono nel PATH
                    sh 'command -v docker || echo "Docker not found"'
                    sh 'command -v podman || echo "Podman not found"'
                    sh 'command -v buildah || echo "Buildah not found"'
                    echo "=== Checking PATH ==="
                    sh 'echo $PATH'
                }
            }
        }
    }
}