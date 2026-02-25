pipeline {
    agent {
        docker { image 'python:3.12.3' }
    }
    environment {
        SONARQUBE_SERVER = 'my_sonarqube'
        SONAR_PROJECT_KEY = 'simple_django_app' 
    }
    stages {
        stage('Self Test') {
            steps {
                sh 'python3 manage.py test'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONARQUBE_SERVER) {
                    sh 'sonar-scanner'
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to SonarQube quality gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }
        stage('CD') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh 'echo "Running CD step..."'
                // Add your CD commands here
            }
        }
    }
}
