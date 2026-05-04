import requests
import time
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def test_idempotency():
    print("\n--- Testing Idempotency ---")
    endpoint = f"{BASE_URL}/feedback/submit"
    idempotency_key = str(uuid.uuid4())
    
    payload = {
        "user_id": 1,
        "inflation_report": "Inflation is making food very expensive.",
        "additional_comments": "Testing idempotency"
    }
    
    headers = {"Idempotency-Key": idempotency_key}
    
    # First request
    print("Sending first request...")
    res1 = requests.post(endpoint, json=payload, headers=headers)
    try:
        res1_json = res1.json()
        print(f"Status: {res1.status_code}, Body: {res1_json}")
    except Exception:
        print(f"Status: {res1.status_code}, Raw Body: {res1.text}")
        return

    # Second request with same key
    print("Sending second request with SAME key...")
    res2 = requests.post(endpoint, json=payload, headers=headers)
    try:
        res2_json = res2.json()
        print(f"Status: {res2.status_code}, Body: {res2_json}")
    except Exception:
        print(f"Status: {res2.status_code}, Raw Body: {res2.text}")
        return
    
    if res1.status_code == 201 and res1_json == res2_json:
        print("SUCCESS: Idempotency confirmed (Identical responses)")
    else:
        print(f"FAILURE: Idempotency check failed. Status: {res1.status_code}")

def test_rate_limiting():
    print("\n--- Testing Rate Limiting ---")
    endpoint = f"{BASE_URL}/feedback/submit"
    
    payload = {
        "user_id": 1,
        "inflation_report": "Rate limit test report",
        "additional_comments": "Testing"
    }

    print("Flooding endpoint (Limit: 5 per minute)...")
    for i in range(7):
        # Use a fresh idempotency key each time to avoid cache hit
        headers = {"Idempotency-Key": str(uuid.uuid4())}
        res = requests.post(endpoint, json=payload, headers=headers)
        print(f"Request {i+1}: Status {res.status_code}")
        
        if res.status_code == 429:
            print(f"SUCCESS: Rate limit triggered! {res.json()['detail']}")
            return

    print("FAILURE: Rate limit was not triggered after 7 requests.")

if __name__ == "__main__":
    try:
        test_idempotency()
        test_rate_limiting()
    except requests.exceptions.ConnectionError:
        print("ERROR: Server is not running. Start it with 'uvicorn app.main:app --reload'")
