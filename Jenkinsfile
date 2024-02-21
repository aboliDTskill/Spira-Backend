pipeline{
    agent any
    environment {
        // Define SSH credentials ID configured in Jenkins
        SSH_CREDENTIALS = '2'
    }
    
    stages {
        
        
    
        stage('Setup Python Virtual ENV for dependencies'){
            steps  {
                script{
                        def sshcm_1=    sh '''
                        chmod +x envsetup.sh
                        ./envsetup.sh
                        '''
                    sshcm_1(script: sshcm_1, remote: '13.200.63.189', credentialsId: env.SSH_CREDENTIALS)
                    }

                }
            
        }
        stage('Setup Gunicorn Setup'){
            steps {
                script{
                    def sschm_2 = sh '''
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
                sshcm_2(script: sshcm_2, remote: '13.200.63.189', credentialsId: env.SSH_CREDENTIALS)
                }
                
            }
        }
        stage('setup NGINX'){
            steps {
                script{
                    def sschm3 = sh '''
                chmod +x nginx.sh
                ./nginx.sh
                '''
                sshcm_3(script: sshcm_2, remote: '13.200.63.189', credentialsId: env.SSH_CREDENTIALS)
                }
                
            }
        }
    }
}


