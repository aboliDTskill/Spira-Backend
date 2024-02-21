pipeline{
    agent any
    environment {
        SSH_KEY               = credentials('spira') // Referencing the SSH key credential
        REMOTE_USER           = 'ubuntu'
        REMOTE_HOST           = '13.200.63.189'
    }
    stages {
    
        stage('Setup Python Virtual ENV for dependencies'){
            steps  {
            sh '''
            chmod +x envsetup.sh
            ./envsetup.sh
            '''}
        }
        stage('Setup Gunicorn Setup'){
            steps {
                sh '''
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }
        stage('setup NGINX'){
            steps {
                sh '''
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }
    }
}