pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '--user root'  // Run as root
        }
    }

    environment {
        EC2_HOST = credentials('EC2_HOST')          // EC2 instance IP
        EC2_USER = credentials('EC2_USER')          // EC2 username (e.g., ubuntu)
        SSH_KEY_ID = credentials('cbde2a97-22ad-4d2c-8d12-932d1fecda79')      // ID of the SSH private key credential in Jenkins
    }

    stages {
        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    apt-get update && apt-get install -y openssh-client
                    
                    # Ensure pip is installed and upgraded
                    python3 -m ensurepip
                    python3 -m pip install --upgrade pip
                    
                    # Install required dependencies
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Retrain the Model') {
            steps {
                sh '''
                    python3 train.py
                '''
            }
        }

        stage('Deploy Model to EC2') {
            steps {
                sshagent(credentials: ["cbde2a97-22ad-4d2c-8d12-932d1fecda79"]) {
                    sh '''
                        # Ensure the model directory exists on EC2
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "mkdir -p /home/${EC2_USER}/models && chmod 755 /home/${EC2_USER}/models"

                        # Copy the trained model to EC2
                        scp -o StrictHostKeyChecking=no models/model_*.pkl ${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/models/
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Model retrained and deployed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}