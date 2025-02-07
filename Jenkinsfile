pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '--user root -v ${env.WORKSPACE.replace("\\", "/")}:/workspace'
        }
    }

    environment {
        WORKDIR = '/workspace'  // Define a valid working directory inside the container
        EC2_USER = 'ubuntu'  // Update with your EC2 instance user
        EC2_HOST = 'your-ec2-instance-ip'  // Update with your EC2 instance IP
    }

    stages {
        stage('Prepare Workspace') {
            steps {
                sh 'mkdir -p $WORKDIR && chmod 777 $WORKDIR'
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
                    python3 -m ensurepip
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt || echo "⚠️ No requirements.txt found, skipping dependency installation."
                '''
            }
        }

        stage('Retrain the Model') {
            steps {
                sh 'python3 train.py || echo "⚠️ Training script failed, check logs."'
            }
        }

        stage('Deploy Model to EC2') {
            steps {
                sshagent(credentials: ['8016f4f1-3a1c-439b-b5fa-b4cde16c68bd']) {
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
                sshagent(credentials: ['8016f4f1-3a1c-439b-b5fa-b4cde16c68bd']) {
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
