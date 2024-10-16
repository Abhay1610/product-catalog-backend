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

# Function to verify the token
def verify_token(token: str):
    try:
        # Decode the token (replace 'your-secret' with the appropriate key from Keycloak)
        payload = jwt.decode(token, 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy5vdv/XDqlAa+/z2J8NdlogWAA+1oDkSIl4ILmpoNy/WQQBVrmP44EHwBtdBip2dKFBCtw8xxUOS9GbNSCMdmcNzwyb+XXlop0h2aHZOr1VQmMhUgSwuJWsS200V1gDk+p2i1O8VPTYF8ibPfvVbOZh1thx4LTdlKlEhancr9rDFsgrefdXgXkzYNkJGQhyPBVOgppxTv66B0NJL+ZwkLZV0ob/HhZOj/ZorQv9nX6z6ZYrZEeUF41ZHM9d7P6Us9gN8ln9S9EypryfRLQ/wM+aSt0JmozcglhVSS58xPJaeA63bUrZm4vgMHkcilqBAcEgdonjwpElX/ik6Keg6uQIDAQAB', algorithms=['RS256'])  
        return payload  # Token is valid
    except JWTError:
        raise Exception("Invalid or expired token")

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
