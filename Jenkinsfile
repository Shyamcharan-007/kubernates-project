pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        DOCKERHUB_USERNAME = 'shyamcharan'
        IMAGE_REPO = 'shyamcharan/fastapi-demo'
        EKS_CLUSTER_NAME = 'Shyam-cluster'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running FastAPI application tests'

                sh '''
                    docker run --rm \
                    -v "$WORKSPACE:/app" \
                    -w /app \
                    python:3.12-slim \
                    sh -c "pip install --no-cache-dir -r requirements.txt && pytest -v"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'

                sh '''
                    docker build \
                    -t "$IMAGE_REPO:$BUILD_NUMBER" \
                    -t "$IMAGE_REPO:latest" .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                        -u "$DOCKER_USER" --password-stdin

                        docker push "$IMAGE_REPO:$BUILD_NUMBER"
                        docker push "$IMAGE_REPO:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Amazon EKS') {
            steps {
                echo 'Connecting to Amazon EKS'

                sh '''
                    aws eks update-kubeconfig \
                    --region "$AWS_DEFAULT_REGION" \
                    --name "$EKS_CLUSTER_NAME"

                    kubectl apply -f k8s/

                    kubectl set image \
                    deployment/fastapi-deployment \
                    fastapi-container="$IMAGE_REPO:$BUILD_NUMBER"

                    kubectl rollout status \
                    deployment/fastapi-deployment \
                    --timeout=180s
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the Jenkins console output.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}