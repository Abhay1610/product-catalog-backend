import requests

# Function to authenticate the user
def authenticate_user(username: str, password: str):
    auth_url = "http://your-keycloak-server/auth/realms/your-realm/protocol/openid-connect/token"  # Update this URL
    auth_data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': 'your-client-id'  # Update with your Keycloak client ID
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
        protected_url = "http://your-fastapi-server/products/protected/"  # Update this URL
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
        user_info_url = "http://your-keycloak-server/auth/realms/your-realm/protocol/openid-connect/userinfo"  # Update with your Keycloak user info URL
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
        logout_url = "http://your-keycloak-server/auth/realms/your-realm/protocol/openid-connect/logout"  # Update with your Keycloak logout URL
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
    username = "your-username"  # Update with your Keycloak username
    password = "your-password"    # Update with your Keycloak password

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
