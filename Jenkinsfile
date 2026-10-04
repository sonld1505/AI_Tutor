pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        GIT_SHA = "${env.GIT_COMMIT}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse --short=12 HEAD',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Factory Validation') {
            steps {
                sh './scripts/factory-jenkins.sh'
            }
        }

        stage('Build') {
            steps {
                sh './scripts/build.sh'
            }
        }

        stage('Lint') {
            steps {
                sh './scripts/lint.sh'
            }
        }

        stage('Unit Test Gate') {
            steps {
                sh './scripts/unit-test.sh'
            }
        }

        stage('Integration Test') {
            steps {
                sh './scripts/integration-test.sh'
            }
        }

        stage('Security Gate') {
            steps {
                sh './scripts/security-scan.sh'
            }
        }

        stage('Build Immutable Artifact') {
            steps {
                sh './scripts/build-artifact.sh'
            }
        }

        stage('Deploy DEV') {
            when {
                branch 'develop'
            }
            steps {
                sh './scripts/deploy.sh dev'
            }
        }

        stage('Deploy STG') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                sh './scripts/deploy.sh stg'
            }
        }

        stage('Deploy UAT') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                sh './scripts/deploy.sh uat'
            }
        }

        stage('Production Approval') {
            when {
                branch 'main'
            }
            steps {
                input(
                    message: "Deploy approved artifact ${env.GIT_SHA} to Production?",
                    ok: 'Deploy'
                )
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            steps {
                sh './scripts/deploy.sh production'
            }
        }
    }

    post {
        success {
            echo 'PIPELINE PASSED'
        }

        failure {
            echo 'PIPELINE FAILED — DEPLOYMENT BLOCKED'
        }

        always {
            archiveArtifacts(
                artifacts: 'factory/logs/**/*',
                allowEmptyArchive: true
            )
        }
    }
}
