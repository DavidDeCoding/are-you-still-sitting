import boto3
import os
import json

client_id = os.environ.get('APP_CLIENT_ID', None)

client = boto3.client('cognito-idp')

def signup(event, context):
    event_body = json.loads(event['body'])
    username = event_body['username']
    password = event_body['password']
    phone_number = event_body['phone_number']
    email = event_body['email']

    response = client.sign_up(
        ClientId=client_id,
        Username=username,
        Password=password,
        UserAttributes=[{
            'Name': 'email',
            'Value': email
        }, {
            'Name': 'phone_number',
            'Value': phone_number
        }]
    )

    if not response['UserConfirmed']:
        return 'Failed'

    return 'Success'

def confirm(event, context):
    event_body = json.loads(event['body'])
    username = event_body['username']
    confirmation_code = event_body['confirmation_code']

    client.confirm_sign_up(
        ClientId=client_id,
        Username=username,
        ConfirmationCode=confirmation_code
    )

    return 'Success'

def login(event, context):
    event_body = json.loads(event['body'])
    username = event_body['username']
    password = event_body['password']

    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )

    if response['AuthenticationResult']:
        return response['AuthenticationResult']['IdToken']

    return 'Failed'
