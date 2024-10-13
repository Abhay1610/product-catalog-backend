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

# Example usage
if __name__ == "__main__":
    username = "your-username"  # Update with your Keycloak username
    password = "your-password"    # Update with your Keycloak password
    products = get_products(username, password)

    if products:
        print("Retrieved products:", products)
