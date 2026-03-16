import os
import random
import time
import requests

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")


def discover_instances(consul_host):
    url = f"http://{consul_host}:8500/v1/health/service/quote-service?passing=true"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        services = resp.json()
        return [
            {
                "id": svc["Service"]["ID"],
                "address": svc["Service"]["Address"],
                "port": svc["Service"]["Port"],
            }
            for svc in services
        ]
    except requests.RequestException as e:
        print(f"Error discovering services: {e}")
        return []


def call_quote_service(instance):
    url = f"http://{instance['address']}:{instance['port']}/quote"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def main():
    print("=== Marcus Aurelius Quote Service Client ===\n")
    print(f"Discovering services via Consul at {CONSUL_HOST}...\n")

    # Retry discovery in case services are still registering
    instances = []
    for attempt in range(5):
        instances = discover_instances(CONSUL_HOST)
        if instances:
            break
        print(f"No instances yet (attempt {attempt + 1}/5), retrying in 3s...")
        time.sleep(3)

    if not instances:
        print("No healthy instances found after retries. Exiting.")
        return

    print(f"Found {len(instances)} healthy instance(s): {[i['id'] for i in instances]}\n")

    for i in range(5):
        instance = random.choice(instances)
        try:
            result = call_quote_service(instance)
            print(f"[{result['instance']}] \"{result['quote']}\"")
            print(f"  — {result['book']}\n")
        except requests.RequestException as e:
            print(f"[{instance['id']}] Error: {e}\n")
        if i < 4:
            time.sleep(1)

    print("=== Done ===")


if __name__ == "__main__":
    main()
