
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Checkout Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/MandyBandaru/ai-devops-incident-assistant.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat '"%PYTHON%" --version'
            }
        }

        stage('Quality Gate - Unit Tests') {
            steps {
                bat '"%PYTHON%" -m unittest discover -v'
            }
        }

        stage('Post-Test Verification') {
            steps {
                echo 'Quality gate passed. All unit tests passed successfully.'
            }
        }
    }
}
