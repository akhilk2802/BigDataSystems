import requests

BASE_API_URL = "http://127.0.0.1:8000"

def login_api(username, password):
    try:
        response = requests.post(
            f"{BASE_API_URL}/login",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, "Invalid username or password."
    except Exception as e:
        return False, f"Error: {e}"

def register_api(username, email, password):
    try:
        response = requests.post(
            f"{BASE_API_URL}/register",
            json={"username": username, "email": email, "password": password},
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Registration failed.")
    except Exception as e:
        return False, f"Error: {e}"
    
def fetch_context(question_id, tool, token):
    try:
        response = requests.post(
            f"{BASE_API_URL}/fetch-context",
            json={"question_id": question_id, "tool": tool},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to fetch context.")
    except Exception as e:
        return False, f"Error: {e}"
    
def response_openai(question, context, model, token):
    try:
        response = requests.post(
            f"{BASE_API_URL}/response-openai",
            json={"question": question, "context": context, "model": model.lower()},
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to get response.")
    except Exception as e:
        return False, f"Error: {e}"