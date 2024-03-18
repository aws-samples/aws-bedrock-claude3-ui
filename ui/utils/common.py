# Copyright iX.
# SPDX-License-Identifier: MIT-0
import ast
import hashlib
import boto3
from botocore.exceptions import ClientError



default_region = "ap-southeast-1"
session = boto3.session.Session(
    region_name = default_region
)
table_name = 'aibox_users'


def verify_user(username, password):
    '''Verify username and password for login'''

    dynamodb = session.resource('dynamodb')
    user_table = dynamodb.Table('aibox_users')

    # Query DynamoDB table for user
    try:
        # resp = user_table.get_item(Key={'userId' : '1001'})
        resp = user_table.get_item(Key={'username': username}) 
    except ClientError as ex:
        # raise ex
        return False

    # Check if user exists
    if 'Item' in resp:
        # Get stored user item
        user = resp['Item']

        # Verify  password
        encrypted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if encrypted_password == user.get('password'):
            return True
        else:
            return False
    else:
        return False


# secret_name = "aitoolkit-login"
def get_secret(secret_name):
    '''Get user dict from Secrets Manager'''
    # Create a Secrets Manager client
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as ex:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise ex

    # Decrypts secret using the associated KMS key.
    secret = ast.literal_eval(response['SecretString'])

    return secret


def translate_text(text, target_lang_code):
    '''
    Supported languages: 
    https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html
    '''
    client = session.client(
        service_name='translate'
    )

    try:
        # Call TranslateText API 
        response = client.translate_text(
            Text=text,  
            SourceLanguageCode='auto', 
            TargetLanguageCode=target_lang_code)
            
        # Get translated text and detected source language code
        translated_text = response['TranslatedText'] 
        source_lang_code = response['SourceLanguageCode']
        
    except ClientError as ex:
        # Log error and set result & source_lang_code to None if fails
        raise ex
        
    return {
        'translated_text':translated_text,
        'source_lang_code':source_lang_code
    }
