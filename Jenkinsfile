pipeline {
    agent { label 'spira-backend-worker' } // Replace 'your-worker-node-label' with the label of your worker node

    stages {
        stage('Setup Python Virtual ENV for dependencies') {
            steps {
                sh '''
                    chmod +x envsetup.sh
                    ./envsetup.sh
                '''
            }
        }

        stage('Setup Gunicorn Setup') {
            steps {
                sh '''
                    chmod +x gunicorn.sh
                    ./gunicorn.sh
                '''
            }
        }

        stage('Setup NGINX') {
            steps {
                sh '''
                    chmod +x nginx.sh
                    ./nginx.sh
                '''
            }
        }
    }
}