// WARNING this file is maintained in the ITK repo, local changes will be
// overwritten as part of the release process.

pipeline {
    agent { label 'default' }
    triggers {
        pollSCM 'H * * * *'
    }
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '25')
        disableConcurrentBuilds()
    }
    stages {
        stage('Build') {
            steps {
                sh 'python3.6 bootstrap.py'
                sh 'bin/buildout -c jenkins.cfg'
            }
        }
        stage('Analysis') {
            steps {
                script {
                    if (fileExists('bin/jenkins-code-analysis')) {
                        sh 'bin/jenkins-code-analysis'
                        sloccountPublish encoding: '', pattern: 'parts/jenkins-test/sloccount.sc', ignoreBuildFailure: true
                        warnings canComputeNew: false,
                            canResolveRelativePaths: false,
                            categoriesPattern: '',
                            canRunOnFailed: true,
                            parserConfigurations: [[parserName: 'a11y-lint', pattern: 'parts/code-analysis/a11y-lint.log'],
                            [parserName: 'chameleon-lint', pattern: 'code-analysis/chameleon-lint.log'],
                            [parserName: 'cleanlines', pattern: 'parts/code-analysis/clean-lines.log'],
                            [parserName: 'importchecker', pattern: 'parts/code-analysis/importchecker.log'],
                            [parserName: 'i18ndude', pattern: 'parts/code-analysis/find-untranslated.log'],
                            [parserName: 'flake8', pattern: 'parts/code-analysis/flake8.log'],
                            [parserName: 'JSLint', pattern: 'parts/code-analysis/jshint.xml'],
                            [parserName: 'stylelint', pattern: 'parts/code-analysis/stylelint.log'],
                            [parserName: 'xmllint', pattern: 'parts/code-analysis/xmllint.log']], unHealthy: '', unstableTotalAll: '0'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    if (fileExists('bin/jenkins-test-karma')) {
                        sh 'bin/jenkins-test-karma'
                    }
                    if (fileExists('bin/jenkins-test-coverage')) {
                        sh 'bin/jenkins-test-coverage'
                    }
                    else if (fileExists('bin/jenkins-test')) {
                        sh 'bin/jenkins-test'
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                if (fileExists('parts/jenkins-test/testreports')) {
                    junit 'parts/jenkins-test/testreports/*.xml'
                }
                if (fileExists('bin/jenkins-test-coverage')) {
                    cobertura autoUpdateHealth: false,
                        autoUpdateStability: false,
                        coberturaReportFile: 'parts/jenkins-test/coverage.xml',
                        conditionalCoverageTargets: '70, 0, 0',
                        failNoReports: false,
                        failUnhealthy: false,
                        failUnstable: false,
                        lineCoverageTargets: '80, 0, 0',
                        maxNumberOfBuilds: 0,
                        methodCoverageTargets: '80, 0, 0',
                        onlyStable: false,
                        sourceEncoding: 'ASCII',
                        zoomCoverageChart: false
                }
            }
        }
        failure {
            stash name: 'workspace', useDefaultExcludes: false
            node('longlived') {
                deleteDir()
                unstash 'workspace'
                script {
                    committerEmail =  sh(script: 'git --no-pager show -s --format=\'%ae\'', returnStdout: true).trim()
                }
                sh "hostname -I > .nodeip"
                emailext body: '${DEFAULT_CONTENT}', subject: '${DEFAULT_SUBJECT}', to: "${committerEmail}"
            }
        }
    }
}
