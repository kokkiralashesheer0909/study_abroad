import boto3
import os
import json
import hmac
import hashlib
import base64

# Initialize AWS Cognito client
cognito = boto3.client('cognito-idp')

# Environment variables
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['COGNITO_CLIENT_ID']
CLIENT_SECRET = os.environ['COGNITO_CLIENT_SECRET']

def calculate_secret_hash(username):
    """
    Calculate the SECRET_HASH required for Cognito API calls, because client secret is enabled in our cognito.
    """
    message = username + CLIENT_ID
    secret = bytes(CLIENT_SECRET, 'utf-8')
    dig = hmac.new(secret, msg=message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def check_user_exists(email):
    """Helper function to check if user exists in Cognito."""
    try:
        cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=email
        )
        return True
    except cognito.exceptions.UserNotFoundException:
        return False

def lambda_handler(event, context):
    try:
        # Parse the incoming JSON body
        body = json.loads(event['body'])
        email = body['email']
        action = body.get('action', 'login')
        
        print(f"Processing {action} request for email: {email}")
        
        # First check if user exists
        user_exists = check_user_exists(email)
        
        if action == 'check':
            return {
                "statusCode": 200 if user_exists else 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "success": user_exists,
                    "message": "User exists" if user_exists else "User not found"
                })
            }
            
        elif action == 'login':
            if not user_exists:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "success": False,
                        "message": "User not found"
                    })
                }
            
            if 'password' not in body:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "success": False,
                        "message": "Password is required"
                    })
                }
            
            try:
                print(f"Attempting login for email: {email}")
                
                # Calculate SECRET_HASH
                secret_hash = calculate_secret_hash(email)
                
                # Authenticate the user with Cognito
                auth_response = cognito.initiate_auth(
                    AuthFlow='USER_PASSWORD_AUTH',
                    ClientId=CLIENT_ID,
                    AuthParameters={
                        'USERNAME': email,
                        'PASSWORD': body['password'],
                        'SECRET_HASH': secret_hash  # Include SECRET_HASH here
                    }
                )
                
                tokens = auth_response.get('AuthenticationResult', {})
                print(f"Login successful for email: {email}")
                
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "success": True,
                        "message": f"Login successful for {email}",
                        "idToken": tokens.get('IdToken'),
                        "accessToken": tokens.get('AccessToken'),
                        "refreshToken": tokens.get('RefreshToken') if body.get('remember', False) else None
                    })
                }
                
            except cognito.exceptions.NotAuthorizedException as e:
                print(f"Invalid credentials for email: {email}. Error: {str(e)}")
                return {
                    "statusCode": 401,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "success": False,
                        "message": f"Incorrect password for email: {email}"
                    })
                }
                
            except cognito.exceptions.UserNotConfirmedException:
                print(f"User not confirmed: {email}")
                return {
                    "statusCode": 403,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST"
                    },
                    "body": json.dumps({
                        "success": False,
                        "message": f"User not confirmed: {email}"
                    })
                }

        else:
            # Handle unknown actions
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({
                    "success": False,
                    "message": "Invalid action specified"
                })
            }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "message": "Internal server error"
            })
        }
