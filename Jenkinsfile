pipeline {
    agent {
        node {
            label 'local'
        }
    }

    stages {
        stage('Check Docker') {
            steps {
                bat 'docker --version'
                bat '"C:\\Users\\vasav\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" version'
            }
        }

        stage('Show Workspace') {
            steps {
                bat 'cd'
                bat 'dir'
            }
        }

        stage('Build Images') {
            steps {
                bat '"C:\\Users\\vasav\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" build'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"C:\\Users\\vasav\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" run --rm webapp pytest -v'
            }
        }

        stage('Deploy Containers') {
            steps {
                bat '"C:\\Users\\vasav\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" up -d'
            }
        }
    }
}