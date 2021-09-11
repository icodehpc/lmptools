pipeline {
    agent any
    stages {
        stage('Setup build environment') {
            steps {
                echo "Installing poetry"
                sh "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.8"
                sh "$HOME/.poetry/bin/poetry install --no-root"
            }
        }
        stage('Run tests') {
            steps {
                sh "$HOME/.poetry/bin/poetry run python3.8 -m pytest tests/*"
            }
        }
    }
}