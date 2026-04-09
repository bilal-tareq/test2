import requests, json

BASE = "https://supercareer-backend-1.onrender.com"
# Using a real-looking email (even if we can't access it, we want to see if the server accepts it)
EMAIL = "test_reset_bilal@gmail.com"

print(f"Testing Forgot Password for {EMAIL}...")
try:
    r = requests.post(f"{BASE}/api/forgot-password/", json={"email": EMAIL}, timeout=45)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
