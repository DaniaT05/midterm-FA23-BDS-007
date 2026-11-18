pipeline {
    agent any
    options { timeout(time: 10, unit: 'MINUTES') }
    environment {
        REG = 'FA23-BDS-007'
        IMAGE = 'midterm-api'
    }
    stages {
        stage('Build and Train') {
            steps {
                sh 'docker build --build-arg GIT_COMMIT=$GIT_COMMIT -t $IMAGE:latest .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run --rm $IMAGE:latest python -m pytest -q tests'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker rm -f $IMAGE || true'
                sh 'docker run -d --name $IMAGE --restart unless-stopped -p 8000:8000 $IMAGE:latest'
            }
        }
        stage('Verify') {
            steps {
                sh '''
                for i in $(seq 1 20); do
                  curl -sf http://localhost:8000/metrics && exit 0
                  sleep 3
                done
                exit 1
                '''
            }
        }
    }
    post {
        always {
            script {
                def metrics = sh(returnStdout: true,
                    script: 'curl -s http://localhost:8000/metrics || echo "metrics unavailable"').trim()
                emailext(
                    to: 'qasimalik@gmail.com',
                    from: 'daniataj.dt@gmail.com',
                    subject: "[${env.REG}] Midterm pipeline ${currentBuild.currentResult} - build #${env.BUILD_NUMBER}",
                    body: "Student Reg No: ${env.REG}\nResult: ${currentBuild.currentResult}\nBuild: ${env.BUILD_URL}\n\nMetrics:\n${metrics}\n"
                )
            }
        }
    }
}