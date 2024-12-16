import os
import requests
import base64


# Global variable to store the token and base url
token = None
expire_time = 18000 # Token expiration time in seconds (5 hour)
base_url = "https://trials5ruji.jfrog.io"


def ping_system_control():
    """
    Sends a ping request to the Artifactory instance.

    Returns:
        str: Response from the Artifactory instance.

    Raises:
        Exception: If the request fails.
    """
    

    url = f"{base_url}/artifactory/api/system/ping"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to ping system: {e}")


def get_system_version_control():
    """
    Sends a request to retrieve the Artifactory system version.

    Returns:
        dict: JSON response containing version details.

    Raises:
        Exception: If the request fails.
    """

    url = f"{base_url}/artifactory/api/system/version"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve system version: {e}")


def list_repositories_control():
    """
    Sends a request to retrieve the list of repositories in Artifactory.

    Returns:
        list: A list of repository details.

    Raises:
        Exception: If the request fails.
    """


    if not base_url or not token:
        raise Exception("Base URL or Identity Token is missing. Please check your .env file.")

    url = f"{base_url}/artifactory/api/repositories"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve repositories: {e}")


def get_storage_info_control():
    """
    Sends a request to retrieve Artifactory's storage information.

    Returns:
        dict: JSON response containing storage details.

    Raises:
        Exception: If the request fails.
    """
    
    if not base_url or not token:
        raise Exception("Base URL or Identity Token is missing. Please check your .env file.")

    url = f"{base_url}/artifactory/api/storageinfo"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve storage info: {e}")


def list_users_control():
    """
    Fetches the list of users from Artifactory.

    Returns:
        list: A list of user details.
        Raises Exception: If the request fails.
    """
    url = f"{base_url}/artifactory/api/users"  # API endpoint to list users
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()  # Returns a list of user details
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve users: {e}")



def create_user_control(username, email, password, admin=False):
    """
    Creates a new user in Artifactory using the correct API endpoint.

    Args:
        username (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.
        admin (bool): Whether the user should have admin privileges.

    Returns:
        dict or int: Returns response status or error message.
    """
    url = f"{base_url}/access/api/v2/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "admin": admin
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        if response.status_code == 201:
            return response.status_code
        else:
            return {"error": f"Unexpected response: {response.status_code}"}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err.response.text}"}
    except Exception as err:
        return {"error": str(err)}


def delete_user_control(username):
    """
    Deletes a user in Artifactory.
    
    Args:
        username (str): The username of the user to delete.

    Returns:
        dict: A success or error message.
    """
    url = f"{base_url}/access/api/v2/users/{username}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"message": f"User: '{username}' has been deleted successfully!"}
        else:
            return {"message": f"Unexpected response: {response.status_code}"}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err.response.text}"}
    except Exception as err:
        return {"error": str(err)}


def create_repository_control(repo_key, repo_type, package_type, remote_url=None):
    """
    Creates a new repository in Artifactory.
    """
    url = f"{base_url}/artifactory/api/repositories/{repo_key}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "rclass": repo_type.lower(),  # e.g., local, remote, virtual
        "packageType": package_type.lower()  # e.g., maven, npm, docker
    }

    if repo_type.lower() == "remote":
        if not remote_url:
            return {"error": "Remote URL is required for remote repositories."}
        payload["url"] = remote_url

    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        if response.status_code == 200:
            return {"message": f"Repository '{repo_key}' created successfully!"}
        else:
            return {"message": f"Unexpected response: {response.status_code}"}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err.response.text}"}
    except Exception as err:
        return {"error": str(err)}
    

def update_repository_control(repo_key, updates):
    """
    Updates an existing repository in Artifactory with provided properties.
    """
    url = f"{base_url}/artifactory/api/repositories/{repo_key}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=updates)
        response.raise_for_status()
        if response.status_code == 200:
            return {"message": f"Repository '{repo_key}' updated successfully!"}
        else:
            return {"message": f"Unexpected response: {response.status_code}"}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err.response.text}"}
    except Exception as err:
        return {"error": str(err)}



def login_control(username, password):
    """
    Generates a token from Artifactory using Basic Auth credentials.

    Args:
        username (str): The username for Artifactory.
        password (str): The password for Artifactory.

    Returns:
        dict: Contains the generated token or an error message.
    """
    url = f"{base_url}/access/api/v1/tokens"  # Endpoint to generate token
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{username}:{password}'.encode()).decode()}",
        "Content-Type": "application/json"
    }
    payload = {
        "scope": "applied-permissions/admin",  # Required scope for admin access
        "expires_in": expire_time  
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        token_data = response.json()  # Parse the response as JSON
        
        global token
        token = token_data["access_token"]
        
        return {"token": token_data.get("access_token", None)}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to generate token: {e}"}
