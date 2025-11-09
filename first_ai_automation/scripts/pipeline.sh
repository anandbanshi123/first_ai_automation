pipeline {
  agent any
  environment {
    RESULTS_DIR = 'results'
    SCREEN_DIR = "${env.RESULTS_DIR}/screenshots"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
        sh 'npx playwright install --with-deps || true'
      }
    }
    stage('Run tests') {
      steps {
        sh '''
          mkdir -p ${RESULTS_DIR}
          pytest -q --junitxml=${RESULTS_DIR}/junit.xml || true
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'results/**', allowEmptyArchive: true
          junit testResults: 'results/junit.xml', allowEmptyResults: true
        }
      }
    }
    stage('Report & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'jira-creds', usernameVariable: 'JIRA_USER', passwordVariable: 'JIRA_API_TOKEN')]) {
          sh '''
            python scripts/test_results_to_jira.py --junit results/junit.xml --screens results/screenshots --jira-base "${JIRA_BASE}" --issue "${JIRA_ISSUE}" --user "${JIRA_USER}" --token "${JIRA_API_TOKEN}" || true
            bash scripts/push_screenshots.sh results/screenshots "ci: add screenshots from ${BUILD_NUMBER}" || true
          '''
        }
      }
    }
  }
}