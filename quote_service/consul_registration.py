import json
import time
import requests


def register_service(consul_host, service_name, instance_name, host, port, max_retries=3):
    url = f"http://{consul_host}:8500/v1/agent/service/register"
    payload = {
        "Name": service_name,
        "ID": instance_name,
        "Address": host,
        "Port": port,
        "Check": {
            "HTTP": f"http://{host}:{port}/health",
            "Interval": "10s",
            "Timeout": "5s",
        },
    }
    for attempt in range(max_retries):
        try:
            resp = requests.put(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
            resp.raise_for_status()
            print(f"[{instance_name}] Registered with Consul at {consul_host}")
            return
        except (ConnectionError, requests.ConnectionError, requests.HTTPError) as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"[{instance_name}] Consul registration failed (attempt {attempt + 1}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Failed to register with Consul after {max_retries} attempts: {e}")


def deregister_service(consul_host, instance_name):
    url = f"http://{consul_host}:8500/v1/agent/service/deregister/{instance_name}"
    try:
        resp = requests.put(url)
        resp.raise_for_status()
        print(f"[{instance_name}] Deregistered from Consul")
    except requests.RequestException as e:
        print(f"[{instance_name}] Warning: failed to deregister from Consul: {e}")
