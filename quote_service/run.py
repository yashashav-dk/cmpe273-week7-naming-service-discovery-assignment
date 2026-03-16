import os
import signal
import sys
from quote_service.app import create_app
from quote_service.consul_registration import register_service, deregister_service

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "quote-svc-1")
SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 5001))
SERVICE_NAME = "quote-service"


def main():
    app = create_app(instance_name=INSTANCE_NAME)

    def shutdown_handler(signum, frame):
        print(f"\n[{INSTANCE_NAME}] Shutting down...")
        deregister_service(consul_host=CONSUL_HOST, instance_name=INSTANCE_NAME)
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    register_service(
        consul_host=CONSUL_HOST,
        service_name=SERVICE_NAME,
        instance_name=INSTANCE_NAME,
        host=INSTANCE_NAME,
        port=SERVICE_PORT,
    )

    app.run(host="0.0.0.0", port=SERVICE_PORT)


if __name__ == "__main__":
    main()
