# 🔧 Jenkins CI/CD Setup Guide

This guide will help you set up Jenkins for automated test execution.

## Prerequisites

- Jenkins server installed and running
- Required Jenkins plugins installed
- Git repository access

## Required Jenkins Plugins

Install these plugins from **Manage Jenkins > Manage Plugins**:

### Essential Plugins
1. **Pipeline** - For Jenkinsfile support
2. **Git** - For source code management
3. **HTML Publisher** - For HTML reports
4. **Allure** - For Allure reports
5. **JUnit** - For test results
6. **Workspace Cleanup** - For workspace management

### Recommended Plugins
7. **AnsiColor** - For colored console output
8. **Timestamper** - For timestamps in logs
9. **Build Timeout** - For build timeouts
10. **Email Extension** - For email notifications
11. **Slack Notification** - For Slack integration
12. **Blue Ocean** - For modern UI

## Step 1: Install Allure Plugin

1. Go to **Manage Jenkins > Manage Plugins**
2. Click **Available** tab
3. Search for "Allure"
4. Install "Allure Jenkins Plugin"
5. Restart Jenkins

## Step 2: Configure Allure

1. Go to **Manage Jenkins > Global Tool Configuration**
2. Scroll to **Allure Commandline**
3. Click **Add Allure Commandline**
4. Name: `allure`
5. Check **Install automatically**
6. Select latest version
7. Save

## Step 3: Create Jenkins Job

### Option A: Pipeline Job (Recommended)

1. Click **New Item**
2. Enter name: `Selenium-BDD-Tests`
3. Select **Pipeline**
4. Click **OK**

#### Configure Pipeline

5. **General**
   - ✅ Discard old builds (Keep last 10)
   - ✅ This project is parameterized
   
6. **Add Parameters:**

   **Browser:**
   - Type: Choice Parameter
   - Name: `BROWSER`
   - Choices: `chrome`, `firefox`, `edge`
   
   **Environment:**
   - Type: Choice Parameter
   - Name: `ENVIRONMENT`
   - Choices: `staging`, `qa`, `production`
   
   **Headless:**
   - Type: Boolean Parameter
   - Name: `HEADLESS`
   - Default: `true`
   
   **Test Suite:**
   - Type: Choice Parameter
   - Name: `TEST_SUITE`
   - Choices: `all`, `smoke`, `regression`, `critical`
   
   **Parallel Workers:**
   - Type: String Parameter
   - Name: `PARALLEL_WORKERS`
   - Default: `4`

7. **Pipeline**
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `<your-repo-url>`
   - Branch: `*/main` or `*/master`
   - Script Path: `Jenkinsfile`

8. **Save**

### Option B: Freestyle Job

1. Click **New Item**
2. Enter name: `Selenium-BDD-Tests-Freestyle`
3. Select **Freestyle project**
4. Click **OK**

#### Configure Freestyle Job

5. **Source Code Management**
   - Select **Git**
   - Repository URL: `<your-repo-url>`
   - Credentials: Add your credentials
   - Branch: `*/main`

6. **Build Environment**
   - ✅ Delete workspace before build starts
   - ✅ Add timestamps to the Console Output

7. **Build Steps**

   Add **Execute shell**:
   ```bash
   # Setup virtual environment
   python3 -m venv venv
   . venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run tests
   pytest -m smoke -n 4 --alluredir=reports/allure-results
   ```

8. **Post-build Actions**

   Add **Allure Report**:
   - Path: `reports/allure-results`
   
   Add **Publish HTML reports**:
   - HTML directory: `reports`
   - Index page: `test_report.html`
   - Report title: `BDD Test Report`
   
   Add **Archive the artifacts**:
   - Files to archive: `reports/**/*`

9. **Save**

## Step 4: Configure Jenkins Environment

### Set Python Path

1. Go to **Manage Jenkins > Configure System**
2. Scroll to **Global properties**
3. Check **Environment variables**
4. Add:
   - Name: `PATH`
   - Value: `/usr/local/bin:$PATH`

### Set Browser Paths (if needed)

Add environment variables:
- `CHROME_BIN=/usr/bin/google-chrome`
- `FIREFOX_BIN=/usr/bin/firefox`

## Step 5: Set Up Credentials

If your repository is private:

1. Go to **Manage Jenkins > Manage Credentials**
2. Click **(global)** domain
3. Click **Add Credentials**
4. Kind: Username with password
5. Scope: Global
6. Username: `<your-username>`
7. Password: `<your-password>`
8. ID: `git-credentials`
9. Description: Git Credentials
10. Click **OK**

## Step 6: Configure Email Notifications (Optional)

1. Go to **Manage Jenkins > Configure System**
2. Scroll to **Extended E-mail Notification**
3. SMTP server: `smtp.gmail.com`
4. SMTP port: `465`
5. Add credentials for email
6. Default recipients: `team@example.com`
7. Save

## Step 7: First Build

### Using Pipeline

1. Go to your pipeline job
2. Click **Build with Parameters**
3. Select options:
   - Browser: `chrome`
   - Environment: `staging`
   - Headless: `true`
   - Test Suite: `smoke`
   - Parallel Workers: `4`
4. Click **Build**

### View Results

1. **Console Output** - Real-time logs
2. **Allure Report** - Detailed test report
3. **HTML Report** - Quick overview
4. **Artifacts** - Screenshots and logs

## Step 8: Schedule Builds (Optional)

### Cron Schedule Examples

1. Edit your job
2. Go to **Build Triggers**
3. Check **Build periodically**
4. Schedule (cron syntax):

```bash
# Every day at 2 AM
0 2 * * *

# Every hour
0 * * * *

# Every Monday at 9 AM
0 9 * * 1

# Every weekday at 6 PM
0 18 * * 1-5
```

5. Save

## Step 9: GitHub Webhook (Optional)

For automatic builds on push:

1. Go to your GitHub repository
2. Settings > Webhooks
3. Click **Add webhook**
4. Payload URL: `http://<jenkins-url>/github-webhook/`
5. Content type: `application/json`
6. Select: **Just the push event**
7. Click **Add webhook**

In Jenkins:
1. Edit your job
2. Build Triggers
3. Check **GitHub hook trigger for GITScm polling**
4. Save

## Troubleshooting

### Issue: Chrome/Firefox not found

**Solution:**
```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Install Firefox
sudo apt-get install firefox
```

### Issue: Python not found

**Solution:**
```bash
# Install Python 3
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### Issue: Permission denied

**Solution:**
```bash
# Give Jenkins user permissions
sudo usermod -aG sudo jenkins
sudo chmod -R 755 /var/lib/jenkins/workspace
```

### Issue: Tests fail in Jenkins but pass locally

**Solution:**
- Ensure `HEADLESS=true` for Jenkins
- Check browser versions match
- Verify all dependencies installed
- Check file paths are relative

## Jenkins Pipeline Stages Explained

### 1. Cleanup
- Deletes old workspace
- Ensures fresh start

### 2. Checkout
- Pulls latest code from Git
- Updates repository

### 3. Setup Python Environment
- Creates virtual environment
- Installs dependencies

### 4. Run Tests
- Executes test suite
- Captures results

### 5. Generate Reports
- Creates HTML report
- Generates Allure report

### 6. Analyze Results
- Calculates pass rate
- Sets build status
- Creates summary

## Best Practices

1. **Use Parameters** - Make builds flexible
2. **Parallel Execution** - Speed up tests
3. **Headless Mode** - Required for CI/CD
4. **Archive Artifacts** - Keep reports
5. **Set Timeouts** - Prevent hanging builds
6. **Clean Workspace** - Avoid conflicts
7. **Version Control** - Track Jenkinsfile changes
8. **Monitor Trends** - Use Allure trends
9. **Notifications** - Alert team on failures
10. **Regular Maintenance** - Update dependencies

## Jenkins Dashboard Metrics

Track these metrics:

- ✅ **Pass Rate** - Target: >95%
- ⏱️ **Build Duration** - Target: <15 min
- 📊 **Test Count** - Track growth
- 🔄 **Build Frequency** - Monitor CI/CD health
- ❌ **Failure Rate** - Identify flaky tests

## Next Steps

1. ✅ Set up Jenkins job
2. ✅ Run first build
3. ✅ View reports
4. ✅ Configure notifications
5. ✅ Set up scheduled builds
6. ✅ Monitor build trends
7. ✅ Optimize performance

## Support

For issues:
1. Check Jenkins console logs
2. Review test execution logs
3. Verify environment variables
4. Check browser installation

---

**Happy CI/CD! 🚀**
