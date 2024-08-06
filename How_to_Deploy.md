## How to Deploy

In the docker_app folder, you will find the streamlit app.

# Prerequisites:

1. python3.8
2. docker
3. Use a Chrome browser for development in Cloud9
4. amazon.titan-image-generator-v1, stability.stable-diffusion-xl-v1, and anthropic.claude-v2 activated in Amazon Bedrock in your AWS account
5. The environment used to create this demo was an AWS Cloud9 m5.24xlarge instance with Amazon Linux 2023, but it should also work with other configurations

# To deploy:

1. Manually create an S3 bucket on the AWS Console
2. Download files from this GitLab and extract zip file
4. Create a Cloud9 environment on the AWS Console
5. Use AWS Configure on the terminal to add your AWS credentials/access keys
6. Upload all files with the same directory structure to Cloud9
7. Edit docker_app/config_file.py, create a STACK_NAME and a CUSTOM_HEADER_VALUE by replacing the ##PLACEHOLDER##. Replace the ##S3_PLACEHOLDER## with the name of the S3 bucket created.
8. Edit cdk/cdk_stack.py, under s3_policy replace the ##S3_PLACEHOLDER## with your S3 bucket name.
9. Install dependencies on the terminal with these commands

- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt

10. Deploy the CDK Template on the terminal with these commands

- cdk bootstrap
- cdk deploy

12. Once deployed, make a note of the output, in which you will find the CloudFront distribution URL and the Cognito user pool id.
13. Create a user in the Cognito UserPool that has been created from the AWS Console.
14. From your Firefox browser, connect to the CloudFront distribution url.
15. Log in to the Streamlit app with the user you have created in Cognito.

