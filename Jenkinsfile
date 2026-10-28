
pipeline {
    agent any

    stages {
        stage('Checkout Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/MandyBandaru/ai-devops-incident-assistant.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat '"C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
            }
        }

        stage('Quality Gate - Unit Tests') {
            steps {
                bat '"C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m unittest -v test_incident_analyzer'
            }
        }

        stage('Post-Test Verification') {
            steps {
                echo 'Quality gate passed. Continuing pipeline.'
            }
        }
    }
}
