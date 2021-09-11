pipeline {
    agent any
    
    stages {
        stage('Setup build environment') {
            steps {
                echo "Installing poetry"
                sh "module load python; which python"
            }
        }
    }
}