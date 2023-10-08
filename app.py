import re
import requests

def is_fake_url(url):
    # Check if the URL starts with a valid scheme (http:// or https://)
    if not re.match(r'^https?://', url):
        return True

    # Check if the domain is an IP address (not a domain name)
    domain = url.split('/')[2]
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
        return True

    # Check for suspicious characters in the domain
    if re.search(r'[^\w\.-]', domain):
        return True

    # Check for common phishing keywords in the URL
    phishing_keywords = ['login', 'password', 'bank', 'secure', 'paypal', 'account']
    if any(keyword in url for keyword in phishing_keywords):
        return True

    return False

def get_wayback_machine_snapshots(url):
    # Wayback Machine API URL
    api_url = f"https://archive.org/wayback/available?url={url}"

    try:
        # Send a GET request to the Wayback Machine API
        response = requests.get(api_url)
        response_json = response.json()

        # Check if snapshots are available
        if 'archived_snapshots' in response_json:
            snapshots = response_json['archived_snapshots']
            if 'closest' in snapshots:
                snapshot_url = snapshots['closest']['url']
                print(f"Snapshot URL: {snapshot_url}")
            else:
                print("No snapshots available for this URL.")
        else:
            print("No snapshots available for this URL.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    user_input = input("Enter a URL to check: ")

    if is_fake_url(user_input):
        print("This URL appears to be fake or suspicious.")
    else:
        print("This URL appears to be legitimate.")
        get_wayback_machine_snapshots(user_input)
