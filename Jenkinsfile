pipeline {
  agent any
  options { timestamps() }
  environment {
    OLLAMA_MODEL = 'qwen2.5-coder:3b'
    OLLAMA_URL   = 'http://127.0.0.1:11434/api/generate'
  }
  stages {
    stage('1. Fetch Code from GitHub') {
      steps {
        sh '''#!/bin/bash
          echo "=== Stage 1: Code checked out by Jenkins from GitHub ===" | tee "$WORKSPACE/build-full.log"
          git -C "$WORKSPACE" log -1 --stat 2>&1 | tee -a "$WORKSPACE/build-full.log" || true
        '''
      }
    }
    stage('2. Build (Maven)') {
      steps {
        sh '''#!/bin/bash
          set -o pipefail
          echo "=== Stage 2: Maven build ===" | tee -a "$WORKSPACE/build-full.log"
          mvn -B clean package 2>&1 | tee -a "$WORKSPACE/build-full.log"
        '''
      }
    }
    stage('3. Security Scan (OWASP / Checkmarx)') {
      steps {
        sh '''#!/bin/bash
          echo "=== Stage 3: [demo stub] OWASP Dependency-Check / Checkmarx scan ===" | tee -a "$WORKSPACE/build-full.log"
        '''
      }
    }
    stage('4. SonarQube + JUnit') {
      steps {
        sh '''#!/bin/bash
          echo "=== Stage 4: [demo stub] SonarQube scan + JUnit publish ===" | tee -a "$WORKSPACE/build-full.log"
        '''
      }
    }
    stage('5. Publish to Nexus') {
      steps {
        sh '''#!/bin/bash
          echo "=== Stage 5: [demo stub] Publish WAR/EAR to Nexus ===" | tee -a "$WORKSPACE/build-full.log"
        '''
      }
    }
    stage('6. Deploy to App Server + Restart') {
      steps {
        sh '''#!/bin/bash
          set -o pipefail
          echo "=== Stage 6: Deploy to Tomcat + restart node ===" | tee -a "$WORKSPACE/build-full.log"
          sudo /opt/deploy-tomcat.sh "$WORKSPACE/target/demo-app.war" 2>&1 | tee -a "$WORKSPACE/build-full.log"
        '''
      }
    }
  }
  post {
    failure {
      echo '============== BUILD FAILED — RUNNING LOCAL-AI ROOT-CAUSE ANALYSIS =============='
      sh '''#!/bin/bash
        python3 "$WORKSPACE/ci/analyze_failure.py" \
          --log "$WORKSPACE/build-full.log" \
          --repo "$WORKSPACE" \
          --model "$OLLAMA_MODEL" \
          --url "$OLLAMA_URL" || true
      '''
    }
    success {
      echo 'Pipeline succeeded — app deployed to Tomcat on port 8888 at /demo-app/hello'
    }
  }
}
