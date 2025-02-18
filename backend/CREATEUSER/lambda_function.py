import boto3
import os
import json
import hmac
import uuid
import hashlib
import base64
from datetime import datetime

# Initialize AWS services
cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')

# Environment variables
USER_POOL_ID = os.environ['USER_POOL_ID']
TABLE_NAME = os.environ['USER_TABLE']
COGNITO_CLIENT_ID = os.environ['COGNITO_CLIENT_ID']
COGNITO_CLIENT_SECRET = os.environ['COGNITO_CLIENT_SECRET']

# Function to calculate SECRET_HASH
def calculate_secret_hash(username):
    message = username + COGNITO_CLIENT_ID
    secret = bytes(COGNITO_CLIENT_SECRET, 'utf-8')  # Encode secret properly
    dig = hmac.new(secret, msg=message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])

        # Extract fields from request
        email = body['email']
        password = body['password']
        first_name = body['firstName']
        last_name = body['lastName']
        phone = body.get('phone', '')
        user_role = body['userRole']

        # Generate unique user ID and custom username
        user_id = str(uuid.uuid4())
        username = f"{first_name.lower()}.{last_name.lower()}{uuid.uuid4().hex[:6]}"

        # Set timestamps
        now = datetime.utcnow().isoformat()

        # Calculate SECRET_HASH
        secret_hash = calculate_secret_hash(username)

        # Step 1: Sign up user in Cognito with SECRET_HASH
        cognito.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=username,
            Password=password,
            SecretHash=secret_hash,  # Include SECRET_HASH here
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'given_name', 'Value': first_name},
                {'Name': 'family_name', 'Value': last_name},
                {'Name': 'phone_number', 'Value': phone},
                {'Name': 'custom:userRole', 'Value': user_role}
            ]
        )

        # Step 2: Confirm user's email (optional)
        # Uncomment this for testing purposes only. In production, users should confirm their email via a verification code/link.
        # cognito.admin_confirm_sign_up(
        #     UserPoolId=USER_POOL_ID,
        #     Username=email
        # )

        # Step 3: Add user to Cognito group based on their role
        cognito.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=username,
            GroupName=user_role  # Ensure this group exists in Cognito (e.g., "student", "faculty", "admin")
        )


        # Step 2: Store user details in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'userId': user_id,
                'username': username,
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'phone': phone,
                'role': user_role,
                'createdAt': now,
                'updatedAt': now
            }
        )

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all origins
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"message": "User signed up successfully", "username": username})
        }

    except cognito.exceptions.UsernameExistsException:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "User already exists."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all origins
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"message": f"Error signing up user: {str(e)}"})
        }



#fix username exists exception
#email verification



