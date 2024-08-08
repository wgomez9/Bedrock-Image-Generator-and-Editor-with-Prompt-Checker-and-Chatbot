## How to Deploy

This guide will walk you through deploying the Streamlit app found in the `docker_app` folder.

### Prerequisites

- Python 3.8
- Docker
- Chrome browser (for development in Cloud9)
- AWS Bedrock models activated:
  - `amazon.titan-image-generator-v1`
  - `stability.stable-diffusion-xl-v1`
  - `anthropic.claude-v2`
- AWS Cloud9 environment (m5.24xlarge instance with Amazon Linux 2023 recommended)

### Deployment Steps

1. **Create S3 Bucket**
   - Manually create an S3 bucket via the AWS Console

2. **Prepare Files**
   - Download files from GitLab and extract the zip file
   - Upload all files to Cloud9, maintaining the directory structure

3. **Set Up Cloud9**
   - Create a Cloud9 environment in the AWS Console
   - Use `aws configure` in the terminal to add your AWS credentials

4. **Configure Application**
   - Edit `docker_app/config_file.py`:
     - Replace `##PLACEHOLDER##` with your chosen `STACK_NAME` and `CUSTOM_HEADER_VALUE`
     - Replace `##S3_PLACEHOLDER##` with your S3 bucket name
   - Edit `cdk/cdk_stack.py`:
     - Under `s3_policy`, replace `##S3_PLACEHOLDER##` with your S3 bucket name

5. **Install Dependencies**
   Run the following commands in the terminal:
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt

6. **Deploy CDK Template**
Execute in the terminal:
- cdk bootstrap
- cdk deploy

7. **Post-Deployment**
- Note the CloudFront distribution URL and Cognito user pool ID from the output
- Create a user in the Cognito User Pool via the AWS Console

8. **Access Application**
- Connect to the CloudFront distribution URL using a Firefox browser
- Log in with your Cognito user credentials

### Note
If you are trying to re-deploy after editing a part of the code, suggestion is to delete the cdk.out folder. If Cloud9 runs out of space, enter command 'docker system prune -a'.


