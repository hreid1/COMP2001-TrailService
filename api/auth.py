import requests

def authenticate_user(email, password, auth_url):
    credentials = {
        'email': email,
        'password': password
    }

    try:
        # If Basic Authentication is needed for the request, include it in the headers
        auth_header = {
            'Authorization': 'Basic ' + requests.auth._basic_auth_str(email, password)
        }
        
        # Send the POST request to authenticate the user
        response = requests.post(auth_url, json=credentials, headers=auth_header)

        # Check for a successful response
        if response.status_code == 200:
            try:
                json_response = response.json()
                return {"status": "success", "data": json_response}
            except ValueError:
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
        # Handle any request-related exceptions
        return {"status": "error", "message": str(e)}
