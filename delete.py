import msal
import requests
import os
import sys

# Confidential Information
CLIENT_ID = os.environ.get('CLIENT')
CLIENT_TOKEN = os.environ.get('CLIENT_SECRET')
TENANT_ID = os.environ.get('TENANT')
EMAIL = os.environ.get('EMAIL_ADDRESS')

AUTHORITY_=f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Create an application
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY_,
    client_credential=CLIENT_TOKEN
)

# Authentication
token = app.acquire_token_for_client(scopes=SCOPES)
if 'access_token' in token:
    access_token = token['access_token']
    print('Access token acquired.')
else:
    print('Error acquiring token:', token.get('error_description'))
    sys.exit()

# API Endpoint - get messages from specifically spam digest
url = f'https://graph.microsoft.com/v1.0/users/{EMAIL}/messages?$top=10'

# filter=from/spam-digest@uillinois.edu
# Requests requires a header
header = {'Authorization': f'Bearer {access_token}'}

response = requests.get(url, headers=header)


# Check if we got a response 
if response.status_code == 200: 
    print("Response Received")
elif response.status_code == 400:
    print("Response Not Found")
    sys.exit()
else:
    print("Unexpected Response - Status Code: " + str(response.status_code))
    sys.exit()

messages = response.json()['value']

for message in messages:
    message_id = message['id']
    print(message_id)

    