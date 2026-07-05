import requests
import jwt
import time
import os

# Create a valid JWT token signed with the default secret
JWT_SECRET = "default_secret_for_local_testing"
token = jwt.encode({"sub": "test-agent"}, JWT_SECRET, algorithm="HS256")

headers = {
    "X-Internal-Auth": token,
    "Content-Type": "application/json"
}

def run_tests():
    print("Testing /health...")
    resp = requests.get("http://127.0.0.1:8000/health")
    print(f"Status: {resp.status_code}, Body: {resp.text}\n")

    print("Testing /.well-known/isli-manifest...")
    resp = requests.get("http://127.0.0.1:8000/.well-known/isli-manifest")
    print(f"Status: {resp.status_code}, Body: {resp.text[:100]}...\n")

    print("Testing /get-exchange-rates...")
    payload = {"currency": "USD"}
    resp = requests.post("http://127.0.0.1:8000/get-exchange-rates", json=payload, headers=headers)
    print(f"Status: {resp.status_code}, Body: {resp.json()}\n")

    print("Testing /get-monetary-stats...")
    payload = {"indicator": "M3"}
    resp = requests.post("http://127.0.0.1:8000/get-monetary-stats", json=payload, headers=headers)
    print(f"Status: {resp.status_code}, Body: {resp.json()}\n")

if __name__ == "__main__":
    # Wait a moment for the server to start if running simultaneously
    time.sleep(2)
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Is it running?")
