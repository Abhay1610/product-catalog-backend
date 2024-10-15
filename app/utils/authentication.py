import requests

# Function to authenticate the user
def authenticate_user(username: str, password: str):
    auth_url = "http://localhost:8080/realms/my-realm/protocol/openid-connect/auth?client_id=account-console&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Frealms%2Fmy-realm%2Faccount&state=0f28a998-089f-46be-989f-23707eeb8c7e&response_mode=query&response_type=code&scope=openid&nonce=421ebaae-5c05-4abb-b2ea-ba22fe2d948b&code_challenge=lovd3bdpDk2WMuL7frO4hmTdFrFmVBGf-Xd-In_bu1s&code_challenge_method=S256"  # Update this URL
    auth_data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': 'my-app'  # Update with your Keycloak client ID
    }
    
    response = requests.post(auth_url, data=auth_data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Authentication failed: " + response.text)

# Function to access the protected endpoint
def get_products(username: str, password: str):
    try:
        access_token = authenticate_user(username, password)
        
        # Access the protected endpoint
        protected_url = "http://localhost:8000/products/protected/"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(protected_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # List of products
        else:
            raise Exception("Failed to retrieve products: " + response.text)
    
    except Exception as e:
        print(e)

# Function to retrieve the user profile
def get_user_profile(token: str):
    try:
        user_info_url = "http://localhost:8000/profile"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # User profile information
        else:
            raise Exception("Failed to retrieve user profile: " + response.text)
    
    except Exception as e:
        print(e)

# Function to log out the user
def logout_user(token: str):
    try:
        logout_url = "http://localhost:8000/logout"  # Update with your Keycloak logout URL
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.post(logout_url, headers=headers)
        
        if response.status_code == 204:
            return {"message": "Logout successful"}
        else:
            raise Exception("Failed to logout user: " + response.text)
    
    except Exception as e:
        print(e)

# Example usage
if __name__ == "__main__":
    username = "myuser"  # Update with your Keycloak username
    password = "myuser@123"    # Update with your Keycloak password

    # Get products
    products = get_products(username, password)
    if products:
        print("Retrieved products:", products)

    # Get user profile
    token = authenticate_user(username, password)  # You can reuse the authentication
    profile = get_user_profile(token)
    if profile:
        print("User profile:", profile)

    # Logout user
    logout_response = logout_user(token)
    if logout_response:
        print(logout_response)
