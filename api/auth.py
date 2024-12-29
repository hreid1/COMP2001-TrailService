import requests

def authenticate_user(email, password, auth_url):
    """
    Authenticate a user with provided credentials against the specified auth URL.
    
    :param email: User's email
    :param password: User's password
    :param auth_url: URL to authenticate the user
    :return: A dictionary containing status and response data
    """
    # Prepare the credentials as a dictionary
    credentials = {
        'email': email,
        'password': password
    }
    
    try:
        # Send POST request to authenticate the user
        response = requests.post(auth_url, json=credentials)
        
        # Handle the response
        if response.status_code == 200:
            try:
                # Attempt to decode the JSON response
                json_response = response.json()
                return {"status": "success", "data": json_response}
            except requests.JSONDecodeError:
                # Handle the case where the response is not valid JSON
                return {"status": "error", "message": "Response is not valid JSON.", "response": response.text}
        else:
            # Handle authentication failure (non-200 status code)
            return {
                "status": "error",
                "message": f"Authentication failed with status code {response.status_code}",
                "response": response.text
            }
    
    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        return {"status": "error", "message": str(e)}

# Example usage
auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
email = 'tim@plymouth.ac.uk'
password = 'COMP2001!'

# Call the function
result = authenticate_user(email, password, auth_url)

# Print the result
if result['status'] == 'success':
    print("Authenticated successfully:", result['data'])
else:
    print(f"Error: {result['message']}")
    print("Response content:", result['response'])
