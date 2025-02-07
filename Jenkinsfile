pipeline {
    agent {
        dockerContainer {
            image 'python:3.10-slim'
            args '--user root'  // Run as root
        }
    }

    environment {
        EC2_HOST = credentials('EC2_HOST')          // EC2 instance IP
        EC2_USER = credentials('EC2_USER')          // EC2 username (e.g., ubuntu)
        SSH_KEY_ID = credentials('8016f4f1-3a1c-439b-b5fa-b4cde16c68bd')  // SSH private key credential in Jenkins
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
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                '''
            }
        }

        stage('Retrain the Model') {
            steps {
                sh '''
                    if [ -f train.py ]; then
                        python3 train.py
                    else
                        echo "train.py not found!"
                        exit 1
                    fi
                '''
            }
        }

        stage('Deploy Model to EC2') {
            steps {
                sshagent(credentials: ["8016f4f1-3a1c-439b-b5fa-b4cde16c68bd"]) {
                    sh '''
                        # Ensure the model directory exists on EC2
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "mkdir -p /home/${EC2_USER}/models && chmod 755 /home/${EC2_USER}/models"

                        # Copy the trained model to EC2
                        if ls models/model_*.pkl 1> /dev/null 2>&1; then
                            scp -o StrictHostKeyChecking=no models/model_*.pkl ${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/models/
                        else
                            echo "No model files found to copy!"
                            exit 1
                        fi
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
