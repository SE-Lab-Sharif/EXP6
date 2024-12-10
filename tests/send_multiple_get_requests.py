import requests
import time
from datetime import datetime


def make_request():
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        response = requests.get("http://localhost:8080/items")
        if response.status_code == 200:
            print(f"[{timestamp}] Request successful")
            return True
        else:
            print(f"[{timestamp}] Error: Status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[{timestamp}] Connection failed - is the load balancer running?")
        return False
    except Exception as e:
        print(f"[{timestamp}] Unexpected error: {str(e)}")
        return False


def main():
    print("Starting load balance test...")
    successful_requests = 0

    for i in range(10):
        if make_request():
            successful_requests += 1
        time.sleep(1)

    print(f"\nCompleted: {successful_requests}/10 successful requests")


if __name__ == "__main__":
    main()
