# Copyright iX.
# SPDX-License-Identifier: MIT-0
import os
import json
import requests
from utils import bedrock, AppConf
from botocore.exceptions import ClientError


# It is recommended to use IAM role authorization
# os.environ["BEDROCK_ASSUME_ROLE"] = "<YOUR_ROLE_ARN>"  # E.g. "arn:aws:..."

# Create new bedrock client
bedrock_runtime = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
)

boto3_bedrock = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
    runtime=False
)

# https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html#model-ids-arns
# model_id = "anthropic.claude-v2:1"
# model_id = 'anthropic.claude-instant-v1'
# model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


def test_connection():
    # Validate the connection
    model_list = boto3_bedrock.list_foundation_models()
    return model_list


def moc_chat(name, message, history):
    history = history or []
    message = message.lower()
    salutation = "Good morning" if message else "Good evening"
    greeting = f"{salutation} {name}. {message} degrees today"
    return greeting


# Helper function to pass prompts and inference parameters
def generate_content(messages, system, params, model_id, runtime=bedrock_runtime):
    """
    Invokes Bedrock LLM to run inference using the input provided in the request body.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/invoke_model.html

    :return: Inference response from the model.
    """

    params['system'] = system
    params['messages'] = messages

    try:
        response = runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(params)
        )

        resp_body = json.loads(response.get('body').read())
        return resp_body

    except ClientError as err:
        print(
            "Invoke LLM faild. Error code: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise


def gene_content_api(messages, system, params, model_id):
   
    if os.getenv('API_SERVER'):
        AppConf.api_server = os.getenv('API_SERVER')
  
    headers = {
        'Content-Type': 'application/json'
    }

    params['system'] = system
    params['messages'] = messages
    params['model'] = model_id
    body=json.dumps(params)

    try:
        response = requests.post(AppConf.api_server, headers=headers, data=body, verify=False)
        response.raise_for_status()
        print(response)
        response_text = json.loads(response.text)
        return response_text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        raise
    