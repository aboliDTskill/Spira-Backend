pipeline{
    agent any
    environment {
        AWS_ACCESS_KEY_ID     = credentials('AKIAZVU3NCIHJICSQCFJ')
        AWS_SECRET_ACCESS_KEY = credentials('T0xSflZcZUSLqGVX/Ks9qExlcD/IHCMyRpR1JqJPHide')
        AWS_REGION            = 'us-east-1'
        SSH_KEY               = credentials('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCr8zXU3J4Nhk04Ahglsqz/vxXoyeaGD0IkFWIz9wIeoj/IPUmhQHLwNlx3vpoN47zvhrLgBMQIMcGCarbu6CUxZlV6y6ptkDgl0vflTFGf1b57jfW86ULeR8+C7oSVuIWp1IqYDEB2cdCm6ThqUNt/CC3TQVfGM5AQupgBQNiTsOsZSt40RG1oyklEAAUoeqDas5C+D5uK5cbLrcyMPoMHFpXObY5WJRilC4WRkO0XjZLMRNcJKfqTJzLUKdGPU4qZwVJMPLKkQNbNWVIPvlv11T9cUUhTRH3gmhKQKdgKamwpPAZgzQWR0OoF7sy2e2z/iGuzEv3UaghrAIUkRG5ackpo6XB4S3ZzuZW5WoIFItnlyFhCV8CGoEdxPYxcsAyZ6RfwAcDyawJ+UclICAlh8tgLe+94QM/Awd33HrhVL/5M8Yx2wjgZ5rLKxiSguKtn23eMlFmiKiPaCHbsmiTonitBP39dg897Ex1LeHH0N/3xcoA6c+Vi9Dv/3Yuv/T8= ubuntu@ip-172-31-35-32') // Referencing the SSH key credential
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