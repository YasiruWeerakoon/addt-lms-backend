import time
from typing import Dict
from jose import jwt

# SECRET KEY (In a real app, hide this in a .env file!)
JWT_SECRET = "super_secret_key_12345" 
JWT_ALGORITHM = "HS256"

# Function to Generate Token
def signJWT(user_id: str, role: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "role": role,
        "expires": time.time() + 6000  # Expires in ~2 hours
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}

# Function to Decode Token (Check if valid)
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}