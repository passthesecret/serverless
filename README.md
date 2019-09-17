# PassTheSecret Serverless

## Introduction

This is the Serverless Application Model (SAM) for the Lambda + API Gateway deployment method for PassTheSecret.

## Test Instructions
```bash
# Install Prerequisites
> pip install -r passthesecret/requirements.txt
# Run Tests
> python -m unittest --verbose
```

## Build Instructions

```bash
# Set the bucket name for deployment artifacts
> CI_BUCKET=passthesecret-ci-bucket
# Set the name for the CloudFormation Stack
> STACK_NAME=PassTheSecret-SAM-DV
# Compute a unique filename for the swagger upload
> SWAGGER_HASH=$(sha256sum swagger.yaml | cut -f1 -d' ')
# Build the SAM Package
> sam build
# Upload the Swagger document for reference later
> aws s3api put-object --bucket $CI_BUCKET --key $SWAGGER_HASH --body swagger.yaml
# Package and upload the Lambda code
> sam package --s3-bucket $CI_BUCKET --output-template-file packaged.yaml
# Execute the CloudFormation stack
> aws cloudformation deploy --stack-name $STACK_NAME --template-file packaged.yaml --no-fail-on-empty-changeset --parameter-overrides SwaggerUri="s3://$CI_BUCKET/$SWAGGER_HASH" --capabilities CAPABILITY_NAMED_IAM
```

## License
PassTheSecret Serverless is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

PassTheSecret Serverless is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with PassTheSecret Serverless.  If not, see <http://www.gnu.org/licenses/>.
