def test_debug_member_creation(client, sample_member_data):
    """Debug test to see what's returned from member creation"""
    response = client.post("/members/", json=sample_member_data)
    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.text}")
    try:
        print(f"Response JSON: {response.json()}")
    except:
        print("Could not parse JSON response")
    # Don't assert anything yet, just see what we get