pipeline{
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('')
        AWS_SECRET_ACCESS_KEY = credentials('')
        AWS_REGION            = 'us-east-1'
        SSH_KEY               = credentials('') // Referencing the SSH key credential
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