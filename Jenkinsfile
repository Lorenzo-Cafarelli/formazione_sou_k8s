/*
 * Pipeline dichiarativa di Jenkins
 * Esegue la build Docker usando Ansible sull'agente.
 */
pipeline {
    // Imposta il nome della pipeline
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    // Specifica l'agente
    // Potresti voler etichettare il tuo agente Rocky/Ansible
    // es. agent { label 'rocky-ansible' }
    agent any

    // Definisce le variabili globali per la pipeline
    environment {
        IMAGE_NAME = 'flask-hello-world' // Nome dell'immagine Docker
        IMAGE_TAG = "build-${BUILD_NUMBER}" // Usa il numero di build per un tag univoco
    }

    // Definisce le fasi (stage) della pipeline
    stages {
        
        // --- STAGE 1: Build dell'immagine Docker via Ansible ---
        stage('Build Docker Image with Ansible') {
            steps {
                echo "Avvio il playbook Ansible per costruire l'immagine: ${IMAGE_NAME}:${IMAGE_TAG}"
                
                // Esegue il comando ansible-playbook
                // -e passa le variabili d'ambiente di Jenkins al playbook
                sh """
                    ansible-playbook build-playbook.yml \
                        -e "image_name=${IMAGE_NAME}" \
                        -e "image_tag=${IMAGE_TAG}"
                """
                
                echo "Build dell'immagine Docker completata con successo."
            }
        }
    }
    
    // Azioni da eseguire al termine della pipeline
    post {
        success {
            echo "Pipeline flask-app-example-build completata con successo."
        }
        failure {
            echo "Pipeline flask-app-example-build fallita."
        }
    }
}

