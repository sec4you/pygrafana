pipeline {
  agent any
  environment {
    PROJECT="pygrafana"
    SONARQUBE="false"
    VERACODE="false"
  }
  stages {
    stage('Build') {
      steps {
        sh 'virtualenv venv ; . venv/bin/activate ; pip install -r requirements.txt ; python setup.py install'
        sh 'python setup.py sdist --formats=gztar,zip'
      }
    }
    stage('Test') {
      steps {
        sh '. venv/bin/activate ; python tests/test_api.py'
      }
    }
    stage('Code Analysis') {
      steps {
        parallel(
          "SonarQube Analysis": {
            script {
              if (SONARQUBE == "true") {
                scannerHome = tool 'sonarqube-scanner';
                withSonarQubeEnv('sonarqube-server') {
                  sh "cp /tmp/${PROJECT}-sonar-scanner.properties /var/jenkins_home/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonarqube-scanner/conf/sonar-scanner.properties ; ${scannerHome}/bin/sonar-scanner"
                }
              }             
            }
          },
          "Veracode Analysis": {
            script {
              if (VERACODE == "true") {
                 withCredentials([usernamePassword(credentialsId: 'VeracodeAPI', passwordVariable: 'veracode_password', usernameVariable: 'veracode_username')]) {
                   veracode applicationName: 'python-app',
                   debug: true,
                   timeout: 480,
                   criticality: 'Medium',
                   scanName: '$timestamp python-app #$buildnumber',
                   createProfile: true,
                   uploadIncludesPattern: 'dist/**.zip',
                   vpassword: "${env.veracode_password}",
                   vuser: "${env.veracode_username}"
                }
	      }
            }
          }
        )
      }
    }
    stage('Nexus Upload') {
      steps {
        sh '. venv/bin/activate ; vers=$(pip freeze | grep "${PROJECT}" | sed -n \"s/${PROJECT}==//p\") ; package=$(echo "dist/${PROJECT}-$vers.tar.gz") ; twine upload $package ; rm -rf dist/*'
      }
    }
  }
}
