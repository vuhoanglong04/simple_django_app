pipeline {
    agent { 
        label 'SonarQube'
    }
    
    environment {
        SONARQUBE_SERVER  = 'my_sonarqube'
        SONAR_PROJECT_KEY = 'simple_django_app'
        DOCKER_CREDENTIALS = 'docker_credentials'
        DOCKER_REPOSITORY = 'longvulinhhoang/simple_django_app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "main", 
                    url: "git@github.com:vuhoanglong04/simple_django_app.git",
                    credentialsId: 'github-ssh'
            }
        }

        stage('Initialize & Test') {
            steps {
                sh """
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                    export PYTHONPATH=.
                    DJANGO_SETTINGS_MODULE=mysite.settings.test ./venv/bin/python manage.py migrate
                    DJANGO_SETTINGS_MODULE=mysite.settings.test ./venv/bin/coverage run --source='.' manage.py test
                    ./venv/bin/coverage xml -o coverage.xml
                    rm -rf venv
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    
                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3 \
                            -Dsonar.sourceEncoding=UTF-8 \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.exclusions=**/migrations/**,manage.py,venv/**
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        '''
                        sh 'docker build -t ${DOCKER_REPOSITORY}:${BUILD_NUMBER} -t ${DOCKER_REPOSITORY}:latest .'
                        sh 'docker push ${DOCKER_REPOSITORY}:${BUILD_NUMBER}'
                        sh 'docker push ${DOCKER_REPOSITORY}:latest'
                        sh 'docker logout'
                    }
                }
            }
        }

        stage('Deploy to Production') {
            agent {
                label 'production'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker pull ${DOCKER_REPOSITORY}:latest
                            docker logout
                        '''
                    }
                    sh '''
                       docker-compose up -d --pull always
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}