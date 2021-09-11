pipeline {
    agent any

    environment {
        PATH = "/usr/local/tools/python/3.8.7/bin:${env.PATH}"
    }
    
    stages {
        stage('Setup build environment') {
            steps {
                echo "Installing poetry"
                sh "which curl"
                sh "which python"
            }
        }
    }
}