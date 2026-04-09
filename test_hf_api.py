import urllib.request

url = "https://bilal340r-supercareer.hf.space/api/docs/"
req = urllib.request.Request(url)

try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("Response:", response.read().decode('utf-8')[:200])
except urllib.error.HTTPError as e:
    print("Status:", e.code)
    try:
        print("Response Content:", e.read().decode('utf-8')[:200])
    except Exception as read_e:
        print("Failed to decode response:", read_e)
except Exception as e:
    print("Error:", e)
