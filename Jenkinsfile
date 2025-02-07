pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '--user root -w /'  // Set working directory to root
        }
    }

    environment {
        DOCKER_HOST = 'tcp://localhost:2375'  // Docker host for Jenkins
        EC2_HOST = credentials('EC2_HOST')          
        EC2_USER = credentials('EC2_USER')          
        SSH_KEY_ID = credentials('8016f4f1-3a1c-439b-b5fa-b4cde16c68bd')  
    }

    stages {
        stage('Prepare Workspace') {
            steps {
                sh 'mkdir -p /workspace'  // Ensure workspace exists
            }
        }

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
                sh 'python3 train.py'
            }
        }

        stage('Deploy Model to EC2') {
            steps {
                sshagent(credentials: ["8016f4f1-3a1c-439b-b5fa-b4cde16c68bd"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            mkdir -p /home/${EC2_USER}/models && chmod 755 /home/${EC2_USER}/models
                        "
                        scp -o StrictHostKeyChecking=no models/model_*.pkl ${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/models/
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sshagent(credentials: ["8016f4f1-3a1c-439b-b5fa-b4cde16c68bd"]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "ls -l /home/${EC2_USER}/models"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Model retrained and deployed successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs for details.'
        }
    }
}
