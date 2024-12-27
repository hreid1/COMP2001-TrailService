import requests

# Authentication details
auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
email = 'tim@plymouth.ac.uk'  # Replace with the user email
password = 'COMP2001!'        # Replace with the user password

# Credentials in JSON format
credentials = {
    'email': email,
    'password': password
}

# Send the authentication request
response = requests.post(auth_url, json=credentials)

# Handle the response
if response.status_code == 200:
    try:
        json_response = response.json()
        print("Authenticated successfully:", json_response)
        
        # Ensure json_response is a dictionary
        if isinstance(json_response, dict):
            # Check if the user is authorized
            if json_response.get('authorized', False):
                print("User is authorized to perform actions.")
                
                # Check if the user is an admin
                if json_response.get('role') == 'admin':
                    print("User is an admin.")
                    # Perform admin actions here
                else:
                    print("User is not an admin.")
            else:
                print("User is not authorized to perform actions.")
        else:
            print("Unexpected response format:", json_response)
    except requests.JSONDecodeError:
        print("Response is not valid JSON. Raw response content:")
        print(response.text)
else:
    print(f"Authentication failed with status code {response.status_code}")
    print("Response content:", response.text)