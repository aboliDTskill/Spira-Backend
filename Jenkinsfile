pipeline {
    
    agent {
        // Specify the label of the node you want to run the pipeline on
        node {
            label 'Spira-dev'
            }
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Define Dockerfile path
                    def dockerfilePath = '/var/lib/jenkins/workspace/Spira-Backend-Dev/Dockerfile'
                    
                    // Build Docker image
                    def dockerImage = docker.build("spira-backend${env.BUILD_NUMBER}", "-f ${dockerfilePath} .")
                    
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    // Run Docker container from the built image
                    sh "docker run -d -p 8000:8000 --name spira-backend-dev${env.BUILD_NUMBER} spira-backend${env.BUILD_NUMBER}"
                }
            }
        }
    }
    post {
        success {
            echo 'Docker image built and container running successfully'
        }
        failure {
            echo 'Failed to build Docker image or run Docker container'
        }
    }
}
