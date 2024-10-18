pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''python3 -m pip install -r requirements.txt
python3 -m unittest
'''
      }
    }

  }
}