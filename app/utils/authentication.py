import requests
from jose import JWTError, jwt

# Keycloak settings
KEYCLOAK_SERVER_URL = "http://localhost:8080/auth/"
REALM_NAME = "my-realm"
CLIENT_ID = "my-app"
CLIENT_SECRET = "RURUfJ6apb5hN6Ca3Enf8mkZWAB4TGvO"  # Keep this secure

# Function to authenticate the user
def authenticate_user(username: str, password: str):
    token_url = f"{KEYCLOAK_SERVER_URL}realms/{REALM_NAME}/protocol/openid-connect/token"
    auth_data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    response = requests.post(token_url, data=auth_data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Authentication failed: " + response.text)

# Function to introspect the token
def introspect_token(token: str):
    introspect_url = f"{KEYCLOAK_SERVER_URL}realms/{REALM_NAME}/protocol/openid-connect/token/introspect"
    auth_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'token': token,
    }
    
    response = requests.post(introspect_url, data=auth_data)
    
    if response.status_code == 200:
        introspect_data = response.json()
        if introspect_data.get('active'):
            return introspect_data  # Token is valid and active
        else:
            raise Exception("Token is invalid or expired")
    else:
        raise Exception("Failed to introspect token: " + response.text)

# Function to retrieve user profile information
def get_user_profile(token: str):
    user_info_url = f"{KEYCLOAK_SERVER_URL}realms/{REALM_NAME}/protocol/openid-connect/userinfo"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(user_info_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # User profile information
    else:
        raise Exception("Failed to retrieve user profile: " + response.text)

# Function to log out the user
def logout_user(token: str):
    logout_url = f"{KEYCLOAK_SERVER_URL}realms/{REALM_NAME}/protocol/openid-connect/logout"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.post(logout_url, headers=headers)
    
    if response.status_code == 204:
        return {"message": "Logout successful"}
    else:
        raise Exception("Failed to logout user: " + response.text)
