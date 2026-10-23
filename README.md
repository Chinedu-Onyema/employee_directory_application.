[![employee directory application test with Github Actions](https://github.com/Chinedu-Onyema/employee_directory_application./actions/workflows/employee_directory_application.yml/badge.svg)](https://github.com/Chinedu-Onyema/employee_directory_application./actions/workflows/employee_directory_application.yml)

[![AWS](https://codebuild.eu-north-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiMGpJS3kvRGg5dEZQTlNuOUxhVXdKbWtKcmlqTVBROFN4TFZYeU9ZTDFXeG8vQlRvSlRqZ0ptNGRyZHkybm9tQ05nVkpYZmpzM3YrSldhNlp3aEVFRTk0PSIsIml2UGFyYW1ldGVyU3BlYyI6ImQ4c0tuVHpQU2VZRWVZVzIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)


# Employee Directory Application: End-to-End DevOps, CI/CD, Kubernetes & GitOps Deployment

This repository provides comprehensive, multi-stage deployment instructions for the Employee Directory Application, a Python Flask web app. 

This project demonstrates a complete DevOps lifecycle, starting from local development, testing, and CI/CD pipelines (GitHub Actions, AWS CodeBuild, CodeDeploy, CodePipeline), advancing to advanced container orchestration using Docker, Docker Compose, Amazon ECS with AWS Fargate, and culminating in a production-grade, multi-cluster Kubernetes deployment using Amazon EKS and Argo CD for GitOps.

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



## PHASE 3: FULL APPLICATION LIFECYCLE AUTOMATION (CI/CD) WITH AWS CODEPIPELINE

### INTRODUCTION
This phase integrates the previous Build and Test components into a seamless, fully automated software delivery pipeline using AWS CodePipeline. 

This orchestrator will listen for changes in GitHub, automatically trigger the AWS CodeBuild process, and, upon success, prepare the application for deployment. 

This phase moves beyond rigid infrastructure to embrace a fully disposable, scalable GitOps deployment model, laying the final groundwork for high availability across different environments. 

You will construct and secure this highly available, fault-tolerant build and test pipeline, ensuring your cloud infrastructure and application logic are optimized and production-ready.

##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [STEPS TO CREATE A PIPELINE WITH AWS CODEPIPELINE.pdf](https://github.com/user-attachments/files/33831366/5.STEPS.TO.CREATE.A.PIPELINE.WITH.AWS.CODEPIPELINE.pdf)
 
##### VIDEO WALKTHROUGH: https://youtu.be/6ViJvazs_Gw


### STEP-BY-STEP DEPLOYMENT INSTRUCTIONS

This guide provides linear, actionable instructions derived from your documentation (PDF GUIDE) to construct and debug your AWS CI/CD pipeline.

1) Pipeline Initialization and Settings

   Action: Log in to your AWS Management Console.
   Search: Type "CodePipeline" in the search bar and navigate to the service.
   Create: Click on Create pipeline.
   Build Method: In the "Choose creation option" page, under Category, select Build custom pipeline, and click Next.
   Pipeline Name: Enter employee_app_pipeline (or your desired unique name).
   Execution Mode: Select Queued.
   Service Role: Select "New service role" (or "Existing service role" if already created for CodePipeline).
   Leave other defaults and click Next.


2) Add Source Stage (GitHub Integration). This stage configures the pipeline to watch your GitHub repository for changes.

    Source: Under Source provider, select GitHub (via GitHub App).

   Connection:
   Click Connect to GitHub.
   Enter a name (e.g., github_codepipeline) and click Connect to GitHub.
   Click Authorize and follow prompts to authenticate and select your account.
   Click Connect. (Wait for confirmation on the CodePipeline page).
   (DevSecOps Note: This established connection securely creates and attaches an IAM policy to your CodePipeline role.

   Repository Name: Input the exact name of your GitHub repository (e.g., Chinedu-Onyema/employee_directory_application).
   Default Branch: Select MAIN.
   Webhook Events: Locate and UNCHECK the checkbox for Webhook events.
   Click Next.


3) Add Build Stage (CodeBuild Integration).
   This stage integrates the previously created CodeBuild project to perform the buildspec.yml actions (Install, Test, Lint, Format, etc.).

   Build Provider: Select AWS CodeBuild.
   Region: Select your target deployment region.
   Project Name: Select employee_directory_application (or the correct CodeBuild project name).
   Build Type: Select Single build.
   Retry: Ensure "Enable automatic retry on stage failure" is checked.

   Input Artifact: Select Source Artifact.
   (Understanding Artifacts: CodePipeline pulls code from GitHub, compresses it into a .zip file, and stores it in an S3 bucket.
   This .zip file is the Source Artifact.)

   Leave other defaults and click Next.


4) Add Test Stage (CodeBuild for Validation).
   This separate stage can be used for deep validation (like stress testing defined in your hook scripts), separate from the core build.

   Test Provider: Select AWS CodeBuild.
   Region: Select your target region.
   Project Name: Select the same employee_directory_application CodeBuild project.
   Build Type: Select Single build.

   Input Artifact: Change this to BUILD ARTIFACT.
   (Understanding Artifacts:
   In this workflow, CodeBuild downloads the source artifact, runs build/test commands, and produces a new compiled/packaged version stored back in S3 as a Build Artifact).

   Ensure "Enable automatic retry on stage failure" is checked.
   Click Next.


5) Add Deploy Stage (CodeDeploy Preparation).
   This stage prepares the groundwork for deploying your microservices-based application across multiple EC2 instances via CodeDeploy.
   It utilizes the appspec.yml file and hook scripts defined in previous phases.

   Deploy Provider: Select AWS CodeDeploy.
   Region: Select your target region.
   Project Name: Select employee_application_deploy (or your correct CodeDeploy project name).
   Deployment Group: Select your group, such as employee-application-group.
   Input Artifact: Select BUILD ARTIFACT.
   Rollback: Ensure "Configure automatic rollback on stage failure" is checked.
   Click Next.


6) Review and Execute Pipeline.
   Review: Examine all stage configurations on the Review page.
   Create: Click on Create pipeline.
   Observe: Watch the stages execute sequentially.
   You can click individual stages to view detailed logs and debug issues.


Troubleshooting: Resolving S3 AccessDenied Errors in Build Stage
If your pipeline fails in the Test or Build stage with an error similar to AccessDenied... is not authorized to perform: s3:ListBucket on the CodePipeline-managed S3 bucket, take the following actions:
error: AccessDenied: User: arn:aws:sts::... assumes-role/... is not authorized to perform: s3:ListBucket on resource: ...


7) Grant CodeBuild Permissions to CodePipeline S3 Artifact Bucket.
   The automatically generated CodePipeline artifact bucket requires explicit s3:ListBucket permissions for the CodeBuild role to access build artifacts.

   Navigate: Go to IAM and select Roles. Search for the specific service role created for this project (e.g., codebuild-employee_directory_application-service-role).
   Edit Role: Click on the role name, then navigate to the Permissions tab.
   Add Inline Policy: Click Add permissions -> Create inline policy.
   Edit JSON: Click on the JSON tab. Remove default script.
   Paste Policy: Paste the following policy script to allow GetObject and ListBucket permissions for that role:
```
   {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:ListBucket"
          ],
      "Resource": [
        "arn:aws:s3:::*",
        "arn:aws:s3:::*/*"
          ]
    }
  ]
}
```
Review Policy: Click Next.
Name Policy: Enter `codebuild_s3_artifact_bucket_access_policy`.
Create: Click Create policy.
Verify: Confirm that your service role now has this new inline policy attached.


8) Re-release Pipeline
   Navigate back to your pipeline in AWS CodePipeline.
   Click the Release change button to restart the lifecycle.
   Observe all stages execute successfully.
   (Artifact Verification: To see the compressed files CodePipeline created, navigate to the **S3** service and locate the CodePipeline bucket.
   You will find prefixes/folders like `BuildArtif/` and `SourceArtif/` containing the artifacts used in the lifecycle).



## PHASE 4: CONTAINERIZING THE MONOLITH INTO MICROSERVICES WITH DOCKER AND DOCKER COMPOSE

### INTRODUCTION
This phase describes how to containerize the monolithic Flask application using Docker and orchestrate its complementary services using Docker Compose. 

We have already accessed and created a CI/CD pipeline for the application using a monolithic architecture; now, we will design a microservice architecture for this application. 

We will create two Docker images—one for testing and a highly optimized one for production—implement environment variable runtimes for different databases (RDS and DynamoDB), and push these images to Docker Hub to provide the cloud teams with flexible options for running containers in development, test, and production environments.

##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [CREATE DOCKER IMAGES AND CONTAINERS FOR DEV TEST PROD ENVIRONMENTS FOR YOUR FLASK APPLICATION WITH DOCKER AND DOCKER COMPOSE.pdf](https://github.com/user-attachments/files/33832729/6.CREATE.DOCKER.IMAGES.AND.CONTAINERS.FOR.DEV.TEST.PROD.ENVIRONMENTS.FOR.YOUR.FLASK.APPLICATION.WITH.DOCKER.AND.DOCKER.COMPOSE.pdf)

 
##### VIDEO WALKTHROUGH PART 1: https://youtu.be/z5dDCQxSPhw

##### VIDEO WALKTHROUGH PART 2: https://youtu.be/s1E2g_FcGpg


### ACTION PLAN AND DEPLOYMENT GUIDE
This guide is structured linearly, walking you through the transition from a standard monolithic setup to a modern microservices architecture using containerization tools.

### PART 1: ESTABLISHING THE DOCKER DEVELOPMENT/TEST ENVIRONMENT
In this section, we create a basic Docker image to run and test the Flask application locally within an isolated container.

1) Activate Virtual Environment:
   Open Codespaces in your employee_directory_application repository.
   Ensure your virtual environment is active:

   <PRE>virtualenv ~/.virtualenvironment</PRE>
   <PRE>source ~/.virtualenvironment/bin/activate</PRE>

2) Create Dockerfile:
   In the root directory, create a new file named Dockerfile.
   This file contains instructions to build the initial Docker image:

   <PRE>touch Dockerfile</PRE>

3) Define Dockerfile Instructions:
   Populate the Dockerfile.
   This utilizes python:3.12-slim to keep the image lightweight while exclusively installing necessary system libraries like pillow for JPEG/PNG image handling.

4) Authenticating with Docker Hub:
   Verify your Docker installation and log in to Docker Hub.
   If you are automatically logged in with a default `codespacesdev` user, you must log out first and log in with your personal credentials:
   
   <PRE>docker --version</PRE>
   <PRE>docker logout</PRE>
   <PRE>docker login</PRE>

5) Build and Run the Test Image:
   Create a new Docker image for testing (replace `<your-docker-username>` with your actual username).
   When running the container, you must pass the `PHOTOS_BUCKET` environment variable for the application to function; a fake value can be used for this development phase.
   This isolates configuration from the code, allowing the same image to work across different environments with different bucket names.
   Build the image

   <PRE>docker build -t <your-docker-username>/test-flask-app-image:test .</PRE>

   Run the container (Mapping port 8080 to container port 80)
   The application.py must be configured to host="0.0.0.0" and port=80
```
   docker run -p 8080:80 \
      -e PHOTOS_BUCKET=my-test-bucket \
      --name test-container \
      -it <your-docker-username>/test-flask-app-image:test
```

6) Troubleshooting Test Container Errors:
   Upon running the container, you will likely receive a "500 Internal Error" because the application attempts to connect to a MySQL database that has not been created.
   Similar to when deploying with AWS CodeDeploy, you need to provide database connection details to resolve this.

7) Isolate Containers with User-Defined Networks:
   To resolve the database error locally, we will use a dedicated `MariaDB` image.
   First, create a new Docker network to enable communication between the pulled MariaDB image and your test Flask app image.
   User-defined bridge networks resolve containers by name automatically via DNS, whereas the default bridge network requires problematic, changing IP addresses.
   
   <PRE>docker network create test-network</PRE>

8) Run the local database container and create tables:
   Run the MariaDB container on the new `test-network`.
   Once running:
   use `docker exec -i local-db mysql` to copy the `database_create_tables.sql` file into the container.
   This automatically creats the necessary `employee` table within the `employees` database.

   Pull and run MariaDB container on test-network
```
   docker run -d \
    --name local-db \
    --network test-network \
    -e MARIADB_ROOT_PASSWORD=secret \
    -e MARIADB_DATABASE=employees \
    mariadb:10.11-jammy
```

   Wait for local-db to initialize, then create the tables
```
   docker exec -i local-db mysql -u root -psecret employees < database_create_tables.sql
```
 
   Link and Start the Test Container:
   Create a new container that connects both the MariaDB and Flask application containers to the same network, allowing them to communicate by name:

```
docker run -p 8080:80 \
  --network test-network \
  -e PHOTOS_BUCKET=anything \
  -e DATABASE_HOST=local-db \
  -e DATABASE_USER=root \
  -e DATABASE_PASSWORD='secret' \
  -e DATABASE_DB_NAME=employees \
  --name new-test-container \
  -it <your-docker-username>/test-flask-app-image:test
```
   Open the application in your browser. 
   You should see the Employee Directory live and functional. 
   You have successfully tested the application in a Development and Test environment.


### PART 2: ESTABLISHING THE DOCKER PRODUCTION ENVIRONMENT
This section shifts focus to creating a separate production environment outside of AWS. 
 
1) Initialize AWS and Terraform:
   To prepare the production environment, you must download and install the AWS CLI and Terraform installers in Codespaces.
   Authenticate with AWS using:

   <PRE>aws configure</PRE>

2) Create RDS Infrastructure with Terraform:
   In the root directory, create a `main.tf` file.

   <PRE>touch main.tf</PRE>
   
   We are creating this RDS database instance in a public subnet to allow it to communicate with Codespaces outside the VPC.
   Setting `publicly_accessible = true` tells AWS to assign a public IP/DNS record, but this is only effective if the subnet has a network route to the internet.
   Initialize Terraform, plan the resource creation, and apply the changes.

3) Optimize Images using .dockerignore:
   Before building the production image, create a hidden `.dockerignore` file.
   This file prevents heavy dependencies (`virtualenvironment/` directory), secrets (`.env` file), and noisy stuffs (logs, `.git` directory) from being copied into the final Docker image.
   This ensures the production image is lightweight, secure, and does not expose sensitive information when pushed to Docker Hub.
   Add common wildcards to ignore directories recursively.

4) Create Environment (.env) and Build Production Image:
   Create a hidden `.env` file containing the specific S3 bucket and RDS database output values generated previously.
   This prevents writing long, messy Docker run scripts and exposing credentials directly in the terminal.
   Build the production image with a 'latest' tag

   <PRE>docker build -t <your-docker-username>/prod-flask-app-image:latest .</PRE>
    
   Compare the size of the production image to the test image; you will observe a significant reduction in size.

5) Initialize the Production Database:
   Similar to the Dev/Test environment, you will get a "500 Internal Error" because the `employee` table does not exist in the new Amazon RDS MySQL database.
   Because we never installed the MySQL CLI inside the production image (only the `mysql-connector-python` library), we must use the existing `mariadb:10.11-jammy` image as a temporary container to connect and create the table directly on the RDS instance over the network.
   Reference environment variables from the .env file.

   <PRE>export $(grep -v '^#' .env | xargs)</PRE>

   Create a container to initialize the RDS database:
```
   docker run -i mariadb:10.11-jammy \
  mysql \
  -h "$DATABASE_HOST" \
  -u "$DATABASE_USER" \
  -p"$DATABASE_PASSWORD" \
  "$DATABASE_DB_NAME" < database_create_tables.sql
```

6) Run the Production Container with AWS Credentials:
   Run the production container by referencing the `.env` file for database connectivity.
   To enable image uploads to S3, the container must authenticate with S3.
   Since we are not in the AWS ecosystem (running on Codespaces), the container cannot authenticate directly; a better alternative is to mount the `aws/` directory where your AWS credentials (access and secret keys) are stored in Codespaces into the container's root path.
   This allows the container to use `boto3` to successfully write to the S3 bucket.
   Run the production container mounting AWS credentials

```
   docker run -p 8080:80 \
      --env-file .env \
      --name prod-container \
      -v ~/.aws:/root/.aws:ro \
      -it <your-docker-username>/prod-flask-app-image:latest
```
   
7) Implementing DynamoDB Runtime Option:
   Create a production environment for a DynamoDB table by adding a DynamoDB resource to your `main.tf` file.
   Set the required partition key named `id` with type `S` (String).
   To switch the application from RDS to DynamoDB, locate the `.env` file and set the `DYNAMO_MODE` environment variable:
```env
    DYNAMO_MODE=1
```
   
   Run the production container again using the same command from step 6. 
   Observe that imputed data is now saved to the DynamoDB table and S3 bucket successfully.


Orchestrating Services with Docker Compose
A regular Docker Compose file would have a database as a separate service, but RDS and DynamoDB are fully-managed AWS services living outside Docker entirely. 
In this scenario, we use only one container service for the Flask app within the Compose file; it just needs a network reachable to the RDS endpoint.


8) Create Docker Compose File: Create a file named `docker-compose.yml`.
   Populate it with the following configuration, ensuring you use the correct `.env` file containing the connection details for your chosen database runtime (RDS or DynamoDB):

```yaml
services:
  app:
    build: .
    container_name: rds-prod-flask-app-container
    ports:
      - "8080:80"
    env_file:
      - .env
    volumes:
      - ~/.aws:/root/.aws:ro
```

9) Start and Stop services: Use Docker Compose to manage the application lifecycle.
    If there were changes in your code, Docker Compose rebuilds the image to ensure it is up to date before starting the container:
    Start the services:

    <PRE>docker compose up</PRE>

    Stop and remove the containers:

    <PRE>docker compose down</PRE>

10) Push Production Image to Docker Hub:
    Log out of the codespaces user and log in with your personal credentials if necessary.
    Identify your production image and push it to Docker Hub:
    
    <PRE>docker login</PRE>
    <PRE>docker push <your-docker-username>/prod-flask-app-image:latest</PRE>

11) Verify and Pull Image:
    Log into your Docker account through the interface to see your repository.
    Click on the Tags tab to see the command to pull your image and run it as a container.

12) Create .gitignore:
    Create a `.gitignore` file to exclude sensitive files (like `.env`, `terraform.tfstate`, and `terraform.tfvars`) and directories (like `aws/` and `.terraform/`) from being pushed to GitHub:

    <PRE>touch .gitignore</PRE>



## PHASE 5: EMPLOYEE DIRECTORY APPLICATION: CONTAINER REGISTRY AND INFRASTRUCTURE SYNC

### INTRODUCTION

This phase describes the process of transitioning from manual AWS resource creation to automated Infrastructure as Code (IaC) management. 

We will create an Amazon Elastic Container Registry (ECR) via the console to act as a secure, private repository for our production Flask application images. 

After authenticating our local Docker environment and pushing the image to AWS, we will utilize the terraform import workflow within GitHub Codespaces. 

This critical step captures the real-world configuration of the ECR repository and injects it into the Terraform state file (terraform.tfstate), enabling Terraform to manage, update, or destroy the repository in the future without config drift.

##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [CREATE AN ECR REPO RESOURCE, PUSH FLASK APP IMAGE AND MANAGE THE ECR RESOURCE WITH TERRAFORM.pdf](https://github.com/user-attachments/files/33835414/8.CREATE.AN.ECR.REPO.RESOURCE.PUSH.FLASK.APP.IMAGE.AND.MANAGE.THE.ECR.RESOURCE.WITH.TERRAFORM.pdf)


##### VIDEO WALKTHROUGH: https://youtu.be/1YIONftfCLM          

### STEP-BY-STEP DEPLOYMENT INSTRUCTIONS

1) Create an ECR Repository via the AWS Console:
   Before pushing images, you must create a repository in AWS to hold them. ECR repositories are private by default.
   Log in to your AWS Management Console.
   Choose your desired Region.
   Search for ECR and navigate to the service.
   Click on Create a repository.

   Configure the Private repository:
   Repository Name: Enter prod-flask-app-image.
   Image Tag Mutability: Select Mutable if you intend to overwrite image tags (like latest) with newer versions.
   Select Immutable to prevent overwriting tags.
   Encryption Settings: Choose AES-256 or use AWS KMS for encryption.
   Image Scanning: Optionally enable Scan on push to automatically check pushed images for security vulnerabilities.

   Click Create.

2) Push the Production Flask Image to ECR.
   With the repository created, you will now push your Docker image.
   AWS provides specific commands tailored to your repository.

   Retrieve Push Commands.
   Click on the name of your newly created repository (prod-flask-app-image).
   Locate and click the View push commands button. A window will open showing commands for Linux/Windows.

   Prepare Image in Codespaces.
   Log in to GitHub and open your employee-directory-application repository in Codespaces.
   Verify you have the required production image locally:

   <PRE>docker images</PRE>

   If the image is not present, pull it from Docker Hub (replace <your-docker-image> with your actual image name):

   <PRE>docker pull edunaking/prod-flask-app-image</PRE>

   Verify the image is now present:

   <PRE>docker images</PRE>

   Authenticate Docker to ECR.
   Go back to the AWS View push commands window and copy the first command.
   This command uses the AWS CLI to generate an authentication token and pipes it to the Docker login command.
   Paste and run the command in your Codespaces terminal.

   Example command (your specific account ID and region will differ)
   <PRE>aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 140023390772.dkr.ecr.eu-north-1.amazonaws.com</PRE>

   Tag and Push the Image:
   Retrieve the Tagging command (the third command) from the AWS push commands window.
   This tags your local image so it can be pushed to the specific ECR repository.
   Run the command, ensuring you use your actual local image name and the ECR repository URI:

   Example (replace placeholders with actual values)
   <PRE>docker tag edunaking/prod-flask-app-image:latest 140023390772.dkr.ecr.eu-north-1.amazonaws.com/prod-flask-app-image:latest</PRE>

   Verify the new tag exists:

   <PRE>docker images</PRE>

   Retrieve and run the Push command (the fourth command) from AWS:

   <PRE>docker push 140023390772.dkr.ecr.eu-north-1.amazonaws.com/prod-flask-app-image:latest</PRE>

   Navigate back to your ECR repository in the AWS Console.
   Under the Images tab, you will now see your pushed image.

3) Synchronize ECR Repository with Terraform.
   Currently, the ECR repository was created manually.
   To bring it under Terraform management, you must use the terraform import workflow.

   Verify Current Terraform State.
   In Codespaces, locate your terraform.tfstate file.
   Ensure your current infrastructure (e.g., RDS, DynamoDB) is deployed and managed. If not, run:

   <PRE>terraform init</PRE>
   <PRE>terraform plan</PRE>
   <PRE>terraform apply</PRE>

4) Add Import Block to Configuration.
   Open your main.tf file.

   Add an import block.
   This block tells Terraform which address in your configuration (to) maps to the specific AWS resource ID (id).
   id: The name of your ECR repository (prod-flask-app-image).
   to: The Terraform resource address you will define next (aws_ecr_repository.flaskapp).
```
import {
  to = aws_ecr_repository.flaskapp
  id = "prod-flask-app-image"
}
```

5) Generate Configuration.
   Initialize Terraform to backend with the new import block:

   <PRE>terraform init</PRE>
   
   Run `terraform plan` with the `-generate-config-out` flag.
   This will extract the actual configuration of the existing ECR repository and write it to a new file:
   
   <PRE>terraform plan -generate-config-out=existing_ecr_resource.tf</PRE>
   Locate the generated `existing_ecr_resource.tf` file in the Codespaces Explorer.
   Copy the `resource "aws_ecr_repository" "flaskapp"` block from the generated file and paste it into your `main.tf` file.
   Delete the temporary file:
   
   <PRE>rm existing_ecr_resource.tf</PRE>

6) Execute the Import.
   Run the `terraform import` command to map the existing AWS resource to your Terraform state file:
   terraform import <terraform_address> <aws_resource_id>

   <PRE>terraform import aws_ecr_repository.flaskapp prod-flask-app-image</PRE>
   Upon success, you should receive a "successful import" message.

7) Verify Sync.
   Examine the `terraform.tfstate` file in the Explorer.
   You will now see the ECR repository configurations have been added to the state and are managed by Terraform.
   Alternatively, verify via the CLI:

   <PRE>cat terraform.tfstate</PRE>
   
   Run a final plan/apply to confirm there is no configuration drift:

   <PRE>terraform apply</PRE>
   
   If successful, you should see no changes made to your infrastructure, confirming that manually created resources are now perfectly in sync with your Terraform configuration.



## PHASE 6: ORCHESTRATING SERVERLESS MICROSERVICES WITH AMAZON ECS, AWS FARGATE, AND GITOPS

### INTRODUCTION

This phase transitions our containerized Flask application to a production-grade, highly available environment using serverless container orchestration. 

We have moved away from rigid monolithic infrastructure to a microservices architecture using Amazon ECS with AWS Fargate, which automatically provisions and manages the underlying compute resources. 

Finally, we implement crucial GitOps practices by using the terraform import workflow to secure Git as the single source of truth, synchronizing our cloud infrastructure state with our Terraform configuration. 

Completing this phase ensures a highly available, fault-tolerant build and test pipeline that reflects modern software development life cycle (SDLC) best practices.


##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [DESIGN A SERVERLESS CONTAINER ORCHESTRATION SERVICE FOR YOUR FLASK APPLICATION WITH ECS AND FARGATE.pdf](https://github.com/user-attachments/files/33837466/7.DESIGN.A.SERVERLESS.CONTAINER.ORCHESTRATION.SERVICE.FOR.YOUR.FLASK.APPLICATION.WITH.ECS.AND.FARGATE.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/PM5rZ5oc_PM


### STEP-BY-STEP ORCHESTRATION AND STATE SYNC GUIDE
This guide details the process from foundational ECR verification to serverless cluster orchestration, runtime error resolution, and automated infrastructure-as-code synchronization. 
DevSecOps principles are applied throughout, using encrypted secrets for secure connections and GitOps as the foundational workflow.

1) Prerequisites and ECR Verification.
   Before orchestrating the lifecycle, verify that the core build pipeline has successfully produced the required artifact.

   Action:
   Confirm that you have completed Phase 4 to create an Amazon ECR repository and successfully push the production monolithic Flask image (prod-flask-app-image) to it.
   This artifact will serve as the source for our microservices deployment.

2) Amazon ECS Serverless Cluster Orchestration.
   This section details setting up a distinct production environment.
   We will establish a serverless ECS cluster using AWS Fargate to automate provision and management of the transient host EC2 instances.

   ECS Cluster Creation:
   Log in to the AWS Management Console and search for ECS.
   Navigate to Clusters -> Create cluster.
   Name the cluster (e.g., prod-flask-app-image-cluster).
   Under Infrastructure advanced, crucially select Fargate ONLY to enable the serverless compute mode.
   Click Create cluster and observe that the cluster initially has nothing running.

   Fargate Task Definition (The Microservices Blueprint):
   A Task Definition defines the microservices, specifying port mappings, environment variables, and memory requirements.
   In the ECS console, select Task Definitions -> Create new task definition.
   Name it (e.g., prod-flask-app-image-task-definition).
```
   Task Definition essentials:
   - launch_type: AWS FARGATE
   - memory: 2 GB
   - essential_container: YES
```

   Browse ECR to select your `prod-flask-app-image` with the tag `latest` as the Image URI. 
   For Port mappings, enable both 80 and 443 (assuming these are the ports your container listens on).

   Secure Environment Variable Injection:
   To separate configuration—things that change between environments—from code, select Add from file for Environment variables.
   Create an `.env` file containing specific secrets previously generated (e.g., `PHOTOS_BUCKET=<your-s3-bucket-name>`).
   Upload this file to an S3 bucket and copy its ARN (e.g., `arn:aws:s3:::my-photos-albums-123/env/25)_environment_variables.env`).
   Paste this ARN path under Location in ECS.


3) Running and Debugging Transient Fargate Tasks.
   This phase covers DevSecOps debugging as the transient hosts might fail initially.
   Keeping environments organized in this manner is reflective of organizations deploying to production.
   While Dev/Test can risk public subnets, production environments must prioritize security, especially with strong public security for cluster resources.

   Deployment options (Task vs. Service):
   Containers can be deployed as a temporary one-off Task (Docker run) or a highly managed Service (orchestration logic integrated with a Load Balancer for high availability, auto-scaling, and auto-restart).
   We will first deploy a one-off Task to validate the blueprint.

   Deploy as a Task:
   Navigate to your Task Definition and select Deploy -> Run Task.
   Under Computed options, choose Capacity provider strategy, set the capacity provider to Fargate or Fargate Spot (cheaper but interruptible), and use the Latest platform version.

   Networking and Security Configuration:
   Under Networking, select your desired VPC, remove ALL Private subnets, and leave ONLY the Public subnet.
   (Operational Note: This avoids dangerous rigid monolithic public IPs to pods that are susceptible to strong attack and implements Load Balancers in public subnets that forward requests to strong security cluster resources in private subnets, prioritized for Kubernetes production).
   Crucial: Check the Public IP is turned ON box.
   Security: Create a new security group (e.g., `task-SG`) and add inbound rules for ports 80 and 443 from Anywhere.
   Click Create.


4) Lifecycle and Runtime Error Resolution.
   This covers the essential debugging required when transient hosts fail due to implicit permissions.
   Debugging S3 Access (Lifecycle Error):
   If your task stops, inspect the logs.
   The transient host might lack implicit permissions, as the automatically created `ecsTaskExecutionRole` may not have S3 bucket permissions to access the `environment_variables.env` file.
   Locate this role in IAM and add the following inline policy:
   
```json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"s3:GetObject"
],
"Resource": "<arn-of-your-file-location>"
},
{
"Effect": "Allow",
"Action": [
"s3:GetBucketLocation"
],
"Resource": "<arn-of-your-s3-bucket>"
}
]
}
```

  Rerun the task with the same configuration. 
  Verify it becomes running, then copy the task's IPv4 address and access it in a browser to see the application serving traffic.
  
  Debugging Database Connectivity (Runtime Error):
  If the application shows a 500 internal error in the browser and the task logs show `mysql.connector.errors.ProgrammingError: 1146 (42502): Table 'employees.employee' doesn't exist`, you must initialize the backend, similar to errors encountered in the development/testing environment.
  Action: Log in to your Codespace environment on GitHub. Update your `.env` file with the fresh connection details (RDS/DynamoDB) from your running ECS task. 
  Execute the terminal commands to initialize the required `employee` table:

  Allow the terminal to read your updated .env file
  
  <PRE>export $(grep -v '^#' .env | xargs)</PRE>
  
  Create the table in the RDS instance using the sql file
```
  docker run -i mariadb:10.11-jammy mysql \
  -h "$DATABASE_HOST" \
  -u "$DATABASE_USER" \
  -p"$DATABASE_PASSWORD" \
  "$DATABASE_DB_NAME" < database_create_tables.sql
```

  Refresh the running ECS task's IPv4 address. 
  The application should now be fully functional with logs showing a Status 200 success code.

5) GitOps Synchronization via Terraform Import workflow.
   We will import and sync the ECS infrastructure and other infrastructure used throughout this project to reference a single point of truth for our cloud infrastructure with Terraform, ensuring Git as the single source of truth.

   State Verification:
   Navigate in Codespaces and locate your `terraform.tfstate` file to see the current managed AWS infrastructure, which should include RDS, DynamoDB, and ECR.
   If these resources don't exist, type the commands below to create them: `terraform init`, `terraform plan`, `terraform apply`.

   Preparing the Import Configuration:
   Add import blocks for the manually created ECS and S3 infrastructure to your `main.tf` file.
   (DevOps Note: Use your exact ECS Cluster Name, the **ARN** of your Task Definition, and your unique S3 Bucket Name respectively):
   main.tf addition.
   
   Import the ECS cluster configuration.
```hcl   
import {
  to = aws_ecs_cluster.host
  id = "prod-flask-app-image-cluster" 
}
```
  
   Import the task definition configuration as a separate resource.
```hcl
import {
  to = aws_ecs_task_definition.config
  id = "arn:aws:ecs:eu-north..." 
}
```

   Import the s3 bucket resource config.
```hcl
import {
  to = aws_s3_bucket.infra
  id = "my-photos-albums-123" 
}
```

   Generating and Merging the HCL Configuration:
   Type the commands below to initialize the backend with your newly added resource blocks and extract the actual configurations into a new, temporary configuration file called `existing_ecs_s3_resources.tf`:

   <PRE>terraform init</PRE>
   <PRE>terraform plan -generate-config-out=existing_ecs_s3_resources.tf</PRE>

   Locate that newly created file in Explorer, COPY all the configurations from it, and **PASTE** them inside your `main.tf` file. 
   Then, DELETE the temporary file (`rm existing_ecs_s3_resources.tf`) from your project.

   Finalizing GitOps Sync:
   Execute the commands below to map the existing AWS configurations to your current Terraform `.tfstate` file:
   
   Import the ECS cluster configuration.
   <PRE>terraform import aws_ecs_cluster.host prod-flask-app-image-cluster</PRE>

   Import the ECS task definition configuration.
   <PRE>terraform import aws_ecs_task_definition.config arn:aws:ecs:eu-north-1:140023390772:task-definition/prod-flask-app-image-task-definition:1</PRE>

   Import the S3 bucket resource config
   <PRE>terraform import aws_s3_bucket.infra my-photos-albums-123</PRE>

   Verify your `terraform.tfstate` file now includes the new infrastructure configurations by typing `cat terraform.tfstate`. 
   Execute a final `terraform apply`. 
   You should now see no changes made to your infrastructure because you have successfully imported and synchronized your manually created ECS and S3 resources with GitOps.

   Operational Note: Use `terraform destroy` to delete all created resources for efficient cleanup. 
   With one command, all these can be replicated in different AWS regions and environments, which makes Terraform a very powerful tool for building cloud infrastructure as code.



## PHASE 7: INTEGRATING GITHUB CONTAINER REGISTRY (GHCR) FOR GITOPS EFFICIENCY

### INTRODUCTION
This phase details how to utilize the GitHub Container Registry (GHCR) as an alternative to Amazon ECR for storing and managing your application's Docker images. 

GHCR allows you to store and manage Docker images directly alongside your source code within the GitHub ecosystem. By keeping code and images in one place, we adhere closely to GitOps principles, allowing for tighter integration, easier permission management using GitHub credentials, and streamlined automated workflows via GitHub Actions. 

Within this phase, we will cover authenticating with GHCR, tagging and pushing images, and managing image lifecycles using both the GitHub UI and the GitHub CLI.


##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [PUSH FLASK APP TO THE GITHUB CONTAINER REGISTRY (GHCR).pdf](https://github.com/user-attachments/files/33841533/9.PUSH.FLASK.APP.TO.THE.GITHUB.CONTAINER.REGISTRY.GHCR.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/LVfoZ9zdvYg


### STEP-BY-STEP DEPLOYMENT INSTRUCTIONS

1) Establish Secure Access to GHCR.
   To push to or pull from GHCR, you must authenticate Docker using a GitHub Personal Access Token (PAT).
   Generate a Personal Access Token (Classic):
   Log in to your GitHub account.
   Navigate to Settings > Developer Settings > Personal access tokens > Tokens (classic).
   Click Generate new token > Generate new token (classic).
   Note: Enter a descriptive name (e.g., "for image/container registry").
   Expiration: Set according to your security policy.

   Select Scopes: You must select the following scopes to control package permissions:
   write:packages (Allows uploading images)
   read:packages (Allows downloading images)
   delete:packages (Allows deleting images)
   read:org (Read-only access to organization-level resources, conditional)

   Click Generate token.
   Important: Copy the generated token immediately. You will not be able to see it again.

   Log in to GHCR via Docker CLI:
   In your terminal (or Codespaces), use the following command to authenticate Docker to ghcr.io.
   Replace placeholders with your token and username.

   <PRE>echo "YOUR_PERSONAL_ACCESS_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin</PRE>
   *Successful login ensures you can push and pull images.*

2) Tag the Application Image for GHCR.
   Before pushing, your existing Docker image must be retagged to match the GHCR URL format: ghcr.io/owner/image_name:tag.

   Identify your existing image:

   <PRE>docker images</PRE>

   Retag the image:
   Use docker tag to create a pointer to your existing image specifically for GHCR.

   <PRE>docker tag existing-image:latest ghcr.io/username/repository-name/image-name:latest</PRE>
   <PRE>docker tag edunaking/prod-flask-app-image:latest ghcr.io/chinedu-onyema/edunaking/prod-flask-app-image:latest</PRE>
   
   *(Note: The provided source material includes an extra organizational layer in the tag format (`ghcr.io/username/org/image`).
   Standard usage is usually `ghcr.io/username/image` or `ghcr.io/org/image`.
   Verify which path structure your specific setup requires).*

3) Push and Verify the Image.
   Push the image to GHCR:

   <PRE>docker push ghcr.io/chinedu-onyema/edunaking/prod-flask-app-image:latest</PRE>

   Verify via UI:
   Go to your GitHub profile and click on the Packages tab.
   You should now see the edunaking/prod-flask-app-image listed.

4) Test Pulling the Image.
   To ensure the image is accessible, attempt to pull it back to your environment.
   If it already exists, Docker will simply overwrite the local copy.

   <PRE>docker pull ghcr.io/chinedu-onyema/edunaking/prod-flask-app-image:latest</PRE>

5) Advanced Image Management via GitHub CLI.
   While you can delete images via the GitHub UI, native Docker CLI commands cannot delete images from a remote registry.
   For command-line management, we use the GitHub CLI (`gh`).

   Authenticate GitHub CLI with PAT.
   When working in GitHub Codespaces, the CLI defaults to using a limited, temporary internal token (`GITHUB_TOKEN`).
   This token does not have the `delete:packages` permission.
   You must switch authentication to the Personal Access Token you have already created.

   Unset the temporary Codespaces token:

   <PRE>unset GITHUB_TOKEN</PRE>

   Log in to the GitHub CLI:

   <PRE>gh auth login</PRE>

   Complete the prompt answers as follows:
   Where do you use GitHub? GitHub.com.
   Preferred protocol for Git operations? HTTPS.
   Authenticate Git with your GitHub credentials? Yes.
   How would you like to authenticate GitHub CLI? Paste an authentication token.
   Paste your authentication token:

   Verify login status:

   <PRE>gh auth status</PRE>

   Delete an Image via CLI.
   To delete the image via API, we need to correctly format the package name. Note that forward slashes (`/`) in the package name must be URL-encoded as `%2F` when making API calls.

   List your containers via API to find details:

   <PRE>gh api /user/packages?package_type=container</PRE>
   *This returns detailed JSON. Locate your package and observe the URL structure (e.g., `.../container/edunaking%2Fprod-flask-app-image`).*

   Execute the DELETE command:
   Use the URL-encoded package name to delete the image.
   <PRE>gh api -X DELETE /user/packages/container/URL_ENCODED_PACKAGE_NAME</PRE>
   <PRE>gh api -X DELETE /user/packages/container/edunaking%2Fprod-flask-app-image</PRE>

   Confirm deletion:
   Rerunning the list command should now return an empty list.
   
   <PRE>gh api /user/packages?package_type=container</PRE>

6) Session Cleanup.
   After completing image management, it is best practice to log out of secure sessions to protect your PAT.

   Log out of GitHub CLI (PAT session):

   <PRE>gh auth logout</PRE>

   Verify GitHub logout:

   <PRE>gh auth status</PRE>

   Log out of Docker GHCR registry:
   
   <PRE>docker logout ghcr.io</PRE>



## PHASE 8: MULTI-CLUSTER EKS DEPLOYMENT WITH ARGO CD

### INTRODUCTION   
This phase describes transitions away from rigid monolithic infrastructure towards a fully disposable, scalable GitOps deployment model. 

We implement DevSecOps principles by treating worker nodes (EC2 instances) as raw, disposable compute engines and using abstract containers (Pods) managed via Git as the single source of truth. 

In this guide, we will constructs and secure a highly available, fault-tolerant build and test pipeline that reflects modern software development life cycle (SDLC) best practices, leveraging Argo CD for continuous comparison and reconciliation.

##### ACCESS PROJECT MATERIALS

##### PDF GUIDE: [COMPREHENSIVE GUIDE TO PRODUCTION READY EKS FOR MULTI CLUSTER DEPLOYMENT FOR A FLASK PP WITH ARGO CD.pdf](https://github.com/user-attachments/files/33843884/10.COMPREHENSIVE.GUIDE.TO.PRODUCTION.READY.EKS.FOR.MULTI.CLUSTER.DEPLOYMENT.FOR.A.FLASK.PP.WITH.ARGO.CD.pdf)

##### VIDEO WALKTHROUGH: https://youtu.be/ahtEWsUEujE


### STEP-BY-STEP DEPLOYMENT GUIDE


1) CREATE IAM ROLES FOR THE EKS CLUSTER AND WORKER NODE GROUP.
   EKS Cluster Role: Create an IAM role named EKSClusterRole using the EKS service use case, attaching the default Amazon EKS cluster policy.
   Node Group Role: Create an IAM role named EKSWorkerNodesRole using the EC2 service use case and attach the managed policies AmazonEKSWorkerNodePolicy, AmazonEKS_CNI_Policy, and AmazonEC2ContainerRegistryReadOnly.

2) CREATE HUB/CENRAL AND SUPPORT EKS CLUSTERS.
   Create a cluster named hub-central using custom configurations with EKS Auto Mode disabled, using EKSClusterRole, allowing cluster administrator access, selecting EKS API and configmap authentication mode, and choosing two public subnets in two different availability zones.
   Configure add-ons such as Amazon VPC CNI and create its role (AmazonEKSPodIdentityAmazonVPCCNIRole), removing External DNS.
   Follow the same steps to create a second cluster named support-cluster using subnets eu-north-1a and eu-north-1b.

3) CREATE WORKER NODES IN A NODE GROUP.
   Select the hub-central cluster, go to Compute, click Add Node Group, name it worker-nodes-group, select EKSWorkerNodesRole, choose an instance type like t3.large, and complete the creation.
   Follow the same steps for the support-cluster.

4) GRANT AN AWS CLI USER EKS CLUSTER PERMISSIONS.
   Go to the hub-central cluster access page, click IAM access entries, select your IAM principal (e.g., onyema_2), and add the access policies AmazonEKSAdminPolicy and AmazonEKSClusterAdminPolicy.
   Repeat the process for the support-cluster.

5) LOG IN TO AWS CLI AND UPDATE KUBERNETES CONFIGURATION (kubectl).
   Install eksctl if needed and update your local kubeconfig for both clusters using the AWS CLI:

   <PRE>aws eks update-kubeconfig --name=hub-central --region=eu-north-1</PRE>
   <PRE>aws eks update-kubeconfig --name=support-cluster --region=eu-north-1</PRE>

   Verify contexts using <PRE>kubectl config get-contexts</PRE> and check pods across namespaces.

6) CREATE KUBERNETES MANIFESTS AND BUILD DOCKER IMAGES.
   Create Kubernetes secrets from your .env file (configured for DynamoDB mode) using kubectl create secret generic flask-app-secrets --from-env-file=.env on your clusters.
   Create an argocd directory containing flask_app_deployment.yml (specifying container port 80 and environment secrets from flask-app-secrets) and flask_app_service.yml.
   Build your Flask application Docker image (e.g., edunaking/prod-flask-app-image:0.2) and push it to Docker Hub. Push code changes to GitHub.


7) INSTALL ARGO CD AND LOG IN VIA THE USER INTERFACE.
   Create the argocd namespace on the hub-central cluster and apply the install manifests:

   <PRE>kubectl create namespace argocd</PRE>
   <PRE>kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml</PRE>

   Configure Argo CD for HTTP protocol by editing the argocd-cmd-params-cm ConfigMap to include server.insecure: "true".
   Edit the argocd-server service type to LoadBalancer to access the Argo CD UI via the external ELB address.
   Retrieve the initial admin password from the argocd-initial-admin-secret secret and decode it using base64 to log into the UI.

8) ADD CLUSTERS TO ARGO CD VIA ARGO CD CLI.
   Install the Argo CD CLI on your local machine and log in:

   <PRE>argocd login <load-balancer-url> --username admin --password <decoded-password> --insecure</PRE>

   Ensure the support-cluster private API endpoint is set to false (endpointPrivateAccess=false, endpointPublicAccess=true) using <PRE>aws eks update-cluster-config</PRE>.
   Add the support cluster to Argo CD:

   <PRE>argocd cluster add <your-cluster-arn> --server <your-load-balancer-url></PRE>

9) DEPLOY THE FLASK APPLICATION TO MULTIPLE EKS CLUSTERS.
   In the Argo CD UI, click Create Application, configure the application name (employee-directory-app-deployment), select the default project, enable automatic sync, point the repository URL to your GitHub repository, set the path to argocd, and select your destination cluster URLs.
   Observe that Argo CD syncs the application successfully, and verify deployments, pods, and services (kubectl get deploy, kubectl get pods, kubectl get svc) on both the hub-central and support-cluster instances. 
