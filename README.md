[![employee directory application test with Github Actions](https://github.com/Chinedu-Onyema/employee_directory_application./actions/workflows/employee_directory_application.yml/badge.svg)](https://github.com/Chinedu-Onyema/employee_directory_application./actions/workflows/employee_directory_application.yml)

[![AWS](https://codebuild.eu-north-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiMGpJS3kvRGg5dEZQTlNuOUxhVXdKbWtKcmlqTVBROFN4TFZYeU9ZTDFXeG8vQlRvSlRqZ0ptNGRyZHkybm9tQ05nVkpYZmpzM3YrSldhNlp3aEVFRTk0PSIsIml2UGFyYW1ldGVyU3BlYyI6ImQ4c0tuVHpQU2VZRWVZVzIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)


# Multi-Environment Deployment of Python Flask Application

This repository provides comprehensive, multi-stage deployment instructions for the Employee Directory Application, a Python Flask web app. 

This project demonstrates a complete DevOps lifecycle, starting from local development, testing, and CI/CD pipelines, advancing to advanced container orchestration using Docker, Docker Compose, Amazon ECS with AWS Fargate, and culminating in a production-grade, multi-cluster Kubernetes deployment using Amazon EKS and Argo CD for GitOps.

The instructions guide you through establishing security best practices like Role-Based Access Control (RBAC), optimizing containers with multi-stage builds and .dockerignore files, and managing cloud infrastructure efficiently with Terraform. 

The project highlights a complete application transformation, including architecture migration from a monolith to microservices and database flexibility between Amazon RDS (MySQL) and Amazon DynamoDB.


## PHASE 1: LOCAL DEVELOPMENT, TESTING, AND CONTINUOUS INTEGRATION

### INTRODUCTION
Before deploying an application, it is crucial to establish a robust local development workflow that includes automated testing, code linting, and formatting. 
This ensures code quality and prevents defects from reaching production.

The first phase guide walks you through setting up a foundational Python environment within GitHub Codespaces. 
You will implement extensive unit and integration tests using pytest to achieve over 90% code coverage. 
This workflow utilizes a Makefile to automate complex commands for dependency installation, testing, linting with pylint, and formatting with black.

Furthermore, this section moves beyond manual testing by introducing GitHub Actions. 
You will construct a YAML workflow file to create a Continuous Integration (CI) pipeline. 
This pipeline automatically triggers these testing and quality assurance tasks whenever code is pushed to the repository, providing immediate feedback on commit health through status badges.

##### ACCESS PROJECT MATERIALS
##### PDF GUIDE 1: [BRANCHING STRATEGIES AND AUTOMATED TESTING (INSTALL TEST LINT FORMAT).pdf](https://github.com/user-attachments/files/33728680/BRANCHING.STRATEGIES.AND.AUTOMATED.TESTING.INSTALL.TEST.LINT.FORMAT.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/0PP6nW51THQ

##### PDF GUIDE 2: [HOW TO SET-UP GITHUB ACTIONS FROM BRANCHING STRATEGIES FOR FLASK APP.pdf](https://github.com/user-attachments/files/33728714/HOW.TO.SET-UP.GITHUB.ACTIONS.FROM.BRANCHING.STRATEGIES.FOR.FLASK.APP.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/Ilk183UXMac


### PART 1: STEPS TO INSTALL, TEST, LINT, AND FORMAT PYTHON APPLICATION FILES

1) Configure Environment:
   Log in to GitHub, navigate to the employee_directory_repository, and open Codespaces. 
   Switch to the pre-existing feature-branch by running:

   <PRE>git switch feature-branch</PRE>

2) Create Test Files:
   Create the necessary Python test files (test_application.py, test_config.py, test_database.py, test_database_dynamo.py, and test_util.py) in your root directory.
   Copy and paste the corresponding test code provided for each file.

3) Update Makefile:
   The Makefile acts as a developer's automation menu.
   Copy and paste the provided script into your Makefile, defining commands for install, test, lint, and format, as well as an all command to execute them sequentially.

4) Update requirements.txt:
   This file lists all project libraries and packages.
   Ensure essential tools for testing (pytest, pytest-cov, pylint) and formatting (black), along with application dependencies (Flask, boto3, etc.), are included by copying    the provided script

5) Install Dependencies:
   Execute the first Makefile command to install all libraries from requirements.txt:

   <PRE>make install</PRE>

   Verify the installed pytest version:
   <PRE>pytest --version</PRE>

6) Run Automated Tests:
   Run individual tests sequentially (e.g., pytest test_application.py -v).
   If you encounter errors, particularly with test_application.py requiring HTML templates, troubleshoot by creating a templates directory and moving the main.html and
   view-edit.html files into it:

   <PRE>mkdir templates</PRE>
   <PRE>mv main.html templates/</PRE>
   <PRE>mv view-edit.html templates/</PRE>

   Re-run the tests.
   To automatically test all files and view a comprehensive code coverage report, use:

   <PRE>make test</PRE>
   (A 97% test code coverage report indicates production-ready code).


7) Lint Code for Quality:
   Analyze code structure and receive warnings about potential issues:
   
   <PRE>make lint</PRE>

   If your pylint score can be improved, consider utilizing an AI model like Claude Haiku 4.5 in the Codespaces chat to identify and resolve linting warnings.
   To remove insignificant error messages from make, add || true to the lint command in your Makefile:
   <PRE>pylint --disable=R,C *.py || true</PRE>


8) Format Code Structure:
   Successfull remove whitespaces, improve indentation, and standardize code logic formatting by running:

   <PRE>make format</PRE>


9) Execute Full Workflow:
   Install dependencies, test, lint, and format all at once:

   <PRE>make all</PRE>


10) Verify Versions:
    To view specific versions of all installed libraries and packages, run:

    <PRE>pip freeze | less</PRE>


11) Save Local Changes:
    Commit your changes to the feature branch:

    <PRE>git status</PRE>
    <PRE>git add .</PRE>
    <PRE>git commit -m "Finished testing locally."</PRE>


### PART 2: STEPS TO SET UP GITHUB ACTIONS FOR AUTOMATED CONTINUOS INTEGRATION (CI)

GitHub Actions automates tasks within your repository. 
In this phase, we move from manual local testing in Codespaces to automated testing whenever code changes occur, particularly when merging from a feature branch to the main branch for production.

1) Preparation:
   Locate the employee_directory_application repo and open Codespaces.
   Verify you are still in the feature-branch, which contains all testing and new files, by checking:

   <PRE>git branch</PRE>
   <PRE>git log</PRE>


2) Merge to Main Branch:
   In a real-world scenario, you would create a pull request before merging, but for this exercise, switch to the main branch and merge the feature branch to it:
   
   <PRE>git checkout main</PRE>
   <PRE>git merge feature-branch</PRE>
   (Observe that the Makefile and test files are now present in the main directory).


3) Sync Remote Repository:
   Pull the latest changes from the remote main branch (GitHub) to ensure synchronization:

   <PRE>git pull origin main</PRE>


4) Create Git Tag:
   Create a specific snapshot tag (e.g., "feb-26-latest-test") to mark this production-ready version of your application:

   <PRE>git tag feb-26-latest-test</PRE>


5) Push Changes and Tag to GitHub:
   Push the changes to the main branch on GitHub, including the newly created tag, so the code is saved remotely and ready for production deployment:

   <PRE>git push</PRE>
   <PRE>git push origin feb-26-latest-test</PRE>


6) Create GitHub Actions Workflow:
   Exit GitHub Codespaces and locate your repo on GitHub.
   Go to the Actions tab and select "set up a workflow yourself".
   An empty main.yml file will open. You can rename it.
   Open the provided workflow configuration file employee_directory_application.yml, then copy and paste its contents into the workflow tab.
   Click Commit changes, allow the default co-pilot generated commit message, and commit again.
   This saves the file within the .github/workflows folder in your repo.


7) Understand the Workflow File (on: push):
   The on: [push] directive triggers this workflow whenever a git push command is executed.
   runs-on: ubuntu-latest specifies that the job runs on GitHub's free Linux-based virtual machines.
   uses: actions/checkout@v2 downloads the repository code so the workflow can access it.
   uses: actions/setup-python@v1 installs the required Python version (e.g., 3.10.18).
   The subsequent run: steps sequentially execute the Makefile commands to install dependencies, run tests with pytest, lint with pylint, and format with black.


8) Monitor Workflow Run:
   Go back to the Actions tab to observe the workflow run and verify all processes are passing.

   
9) Troubleshoot build failure: If your workflow fails, examine the error cause.
   For instance, if you encounter a build failure because a specific Python version (e.g., 3.10.18) is degraded or unavailable on GitHub Actions' Ubuntu servers, edit the
   workflow file to select a suggested alternative version (e.g., 3.12.12) and commit the changes.
   Return to the Actions tab to trigger a new run and verify the build becomes green.


10) Create a Status Badge: Share the successful status of your build and test with your team by creating a status badge.
    Click on the successful workflow run, locate the three dots (...) next to "Re-run all jobs", and select "Create status badge".
    Copy the status badge Markdown, navigate to your repo's README.md file, click edit, paste the badge at the top, and commit the changes.
    Your README will now display the passing badge from GitHub Actions, indicating production-ready code.



## PHASE 2: MASTERING CONTINUOS INTEGRATION WITH AWS CODEBUILD AND PREPARING FOR CODEDEPLOY

### INTRODUCTION
This phase details how to set up robust automated testing within AWS to validate your application before every deployment, followed by the specific architectural steps needed to prepare your application for deployment via AWS CodeDeploy. 

By completing this phase, you will secure your Software Development Life Cycle (SDLC) with a cloud-native build process and lay the critical groundwork—lifecycle scripts and the mandatory appspec.yml file—for Continuous Deployment to EC2 instances. 

DevSecOps principles are heavily emphasized, using encrypted secrets for secure connections and GitOps as the foundational workflow.


##### ACCESS PROJECT MATERIALS

##### PDF GUIDE 1: [BUILD AND TEST WITH AWS CODEBUILD.pdf](https://github.com/user-attachments/files/33763708/3.BUILD.AND.TEST.WITH.AWS.CODEBUILD.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/IbT8WcHYn7M


##### PDF GUIDE 2: [STEPS TO CREATING THE APPSPEC FILE FOR AWS CODEDEPLOY.pdf](https://github.com/user-attachments/files/33763885/4.STEPS.TO.CREATING.THE.APPSPEC.FILE.FOR.AWS.CODEDEPLOY.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/cRlyxyUBGOk


### PART 1: ESTABLISHING CONTINUOUS INTEGRATION WITH AWS CODEBUILD

This section outlines how to configure AWS CodeBuild, the cloud-native equivalent of GitHub Actions, to automatically compile code, run tests, lint for quality, and format style upon every push to your repository, ensuring enterprise-grade software health.

1) Log in and Initialize:
   Action: Log in to your AWS Management Console.
   Search: Search for CodeBuild.
   Navigate: In the CodeBuild dashboard, ensure Build history under Build is visible.
   Click Build projects and then Create project.


2) Configure Project Details:
   Project name: Enter employee_directory_application. (Note: This is illustrative, ensure it matches your specific repository name).
   Project type: Select Default project (to view build and test workflows within AWS).
   Optional Description: Under Additional configuration, you can write a description like "Building and Testing with Codebuild."
   Badge: Under Build badge-optional, check the box.


3) Set up Source (Secure GitHub Connection):
   Source: Under Source 1 -Primary, select GitHub (as your source provider).
   Credentials Setup (via Secrets Manager): To connect, you must secure your GitHub Personal Access Token (PAT). Click Manage account credentials[cite: 13].
   Credential Type: Personal access token.
   Service: Secrets Manager (Recommended).
   Secrets: New secrets.
   Secret Name: GITHUB.
   Optional Description: "This secret allows AWS Codebuild to connect to GitHub.

   Generate Token (within GitHub):
   Navigate in GitHub to Profile Picture -> Settings -> Developer Settings -> Personal Access Tokens -> Fine-grained tokens.
   Generate new tokens named employee-application-token.
   Description: "This is a token for employee build and test on AWS CodeBuild.
   Expiration: Set to 30 days or desired duration.
   Repository Access: Select Public repositories.
   Click Generate token and COPY the token ID/Token.
   Store it securely; you will not see it again.

   Finalize Connection: Paste your generated GitHub token into the authentication page, completing the secure connection.


4) Define Build Triggers and Environment:
   Repository: Select Repository in my account and paste your specific repo's URL, like
   [https://github.com/Chinedu-Onyema/employee_directory_application.git](https://github.com/Chinedu-Onyema/employee_directory_application.git).
   Triggers: The Webhook box must be checked.
   Comment approval: Select Disable.
   Webhook event filter groups: Locate Event type and select PUSH. (This ensures only pushed commits, not pull requests, trigger this specific build).
   Environment Variables: Under Environment -> Locate Environmental variables.

   Secrets Manager Integration (Secure Variable Reference):
   To securely provide variables to the build (like the key referenced as PHOTOS_BUCKET), create variables from Secrets Manager:
   Name: PHOTOS_BUCKET (or the specific key used in your code).
   Value: Paste the specific ARN for this secret from AWS Secrets Manager
   (example format: arn:aws:secretsmanager:eu-north-1:140023390772:secret:employee-application-secrets-rBVR2r).
   Type: Select Secrets Manager. (Alternative: If hardcoding plaintext is necessary, use PLAINTEXT type and enter any test value).


5) Create and Commit buildspec.yml:
   Action: Under Buildspec, select Use a buildspec file.
   Navigate in GitHub:
   Return to your employee_directory_application repository (via Codespaces or direct GitHub interaction) and create a new file named buildspec.yml in the root directory.
   Codespaces terminal:

   <PRR>touch buildspec.yml</PRE>

   Populate buildspec.yml:
   Copy and paste the script below, which utilizes commands derived from your project's Makefile:

```
version: 0.2
phases:
  install:
    commands:
      - make install
  build:
    commands:
      - make test
      - make lint
      - make format
      - make all
```

   **Commit changes:** 
   <PRE>git status</PRE>
   <PRE>git add .</PRE> 
   <PRE>git commit -m "added buildspec.yml file"</PRE> 
   <PRE>git push</PRE> 
   
   (A workflow run in GitHub Actions will also be triggered).
   **Back in AWS CodeBuild:** Under **BUILDSPEC Name Optional**, enter `buildspec.yml`. Leave other defaults and click **Create build project**.


6) Troubleshooting Secrets Manager Policy Errors:
   If your build fails due to a "Secrets Manager policy error" like the one below, take the following actions:
   error: AccessDenied: User: arn:aws:sts::... assumes-role/... is not authorized to perform: secretsmanager:GetSecretValue on resource: ...
   Search for **IAM** and select the service.
   Locate **Roles** and search for the specific service role created for this project (e.g., `codebuild-employee_directory_application-service-role`).
   Click the role -> **Add permissions** -> **Create inline policy**.
   Policy Editor -> Select **JSON**. Remove default script and paste the following policy:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SidGetSecretValue",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
          ],
      "Resource": "*"
    }
  ]
}
```

   Click **Next**. Give the policy a name, such as `codebuildsecretsmanagerinlinepolicy`, and click **Create policy**.
   Verify that your service role now has two policies attached: the CodeBuild base policy and `codebuildsecretsmanagerinlinepolicy`.


7) Verify CI Build and Add Status Badge to GitHub:
   Navigate in AWS CodeBuild and click **Start build**.
   Monitor progress in the **Build logs** tab.
   Check for errors by clicking **View entire logs** or by tailing them. Ensure the build uses instructions from the provided `buildspec.yml` file.
   Upon success, you receive a success message.
   Click the **employee_directory_application** build project.
   Scroll down to the **Project details** tab, click it, and **Copy badge URL**.
   Navigate to your GitHub repository, click on the README file, click edit, and paste the URL from AWS CodeBuild, formatted as: `[![AWS](your_copied_url)]`.
   Click commit changes.
   Observe that a live build badge now displays the successful state of your code in AWS CodeBuild.



### PART 2: PREPARATION FOR AWS CODEDEPLOY TO EC2

This section details the critical steps needed to architect your development environment for deployment, move away from rigid monolithic infrastructure, and create the required lifecycle scripts and AppSpec file necessary for deployment to Linux EC2 instances via AWS CodeDeploy.

1) Synchronize Environments in GitHub Codespaces:
   **Locate repository:** Log in to GitHub, locate your `employee_directory_application` repo, and open Codespaces.
   **Sync Branch:** Ensure your current Codespaces environment is in sync with your remote main branch (GitHub).
   Execute the command:
    
   <PRE>git pull</PRE>
   This will synchronize all changes made manually in the remote main branch (GitHub) to the local main branch (Codespaces).
   It ensures the `buildspec.yml` file is now present in your Codespaces environment.


2) Create Automation Scripts (`scripts/` folder):
   You must create several lifecycle hook scripts to automate the installation of dependencies and initialization of the application on the EC2 target.

   **Create directory:**
   <PRE>mkdir scripts</PRE>
    
   **Create Install Script:** Change to the scripts directory and create `install_dependencies.sh`:
   
   <PRE>cd scripts</PRE>
   <PRE>touch install_dependencies.sh</PRE>
   
   **Populate `install_dependencies.sh`:**

   **Create Setup Script:** create `setup_application.sh`:
    
   <PRE>touch setup_application.sh</PRE>
   
   **Populate `setup_application.sh`:**

   **Create Start Script:** create `start_server.sh`

   <PRE>touch start_server.sh</PRE>

   **Populate `start_server.sh`:**

   **Create Stop Script:** create `stop_server.sh`:

   <PRE>touch stop_server.sh</PRE>

   **Populate `stop_server.sh`:**

   **Create Validate Script:** create `validate_service.sh`:

   <PRE>touch validate_service.sh</PRE>

   **Populate `validate_service.sh`:**


3) Configure Mandatory `appspec.yml` File:
   The `appspec.yml` file is mandatory for CodeDeploy and orchestrates the deployment flow and hook executions on the target EC2 instance[cite: 3, 4].

   **Exit scripts directory:** cd ...
   **Create AppSpec:** `touch appspec.yml`.
   **Populate `appspec.yml`:**


4) Save Changes and Format Scripts:
   **Save changes to GitHub:**
   Commit your new scripts and the `appspec.yml` file

   <PRE>git status</PRE>
   <PRE>git add .</PRE>
   <PRE>git commit -m "added appspec.yml file and scripts for deployment."</PRE>
   <PRE>git push</PRE>

   Verify a new successful workflow run under the GitHub Actions tab.
   **Format Bash Scripts (Optional but Recommended):**
   To ensure proper formatting of your `.sh` files, install and use `shfmt`:
   Install `shfmt` in Codespaces:
   <PRE>wget https://github.com/mvdan/sh/releases/download/v3.13.1/shfmt_v3.13.1_linux_amd64 -O shfmt && chmod +x shfmt && sudo mv shfmt /usr/local/bin/</PRE>
   <PRE>shfmt --version</PRE>

   Change to scripts folder and format all files recursively:

   <PRE>cd scripts</PRE>
   <PRE>shfmt -w install_dependencies.sh</PRE>
   <PRE>shfmt -w setup_application.sh</PRE>
   <PRE>shfmt -w start_server.sh</PRE>
   <PRE>shfmt -w stop_server.sh</PRE>
   <PRE>shfmt -w validate_service.sh</PRE>

   **Save and Push Formatted Changes:**
    
   <PRE>git status</PRE>
   <PRE>git add .</PRE>
   <PRE>git commit -m "added appspec.yml file for deployment."</PRE>
   <PRE>git push</PRE>
   
