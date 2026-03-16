from unittest.mock import patch, MagicMock
from client.client import discover_instances, call_quote_service


@patch("client.client.requests.get")
def test_discover_instances_parses_consul_response(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: [
            {
                "Service": {"ID": "quote-svc-1", "Address": "quote-svc-1", "Port": 5001},
                "Checks": [{"Status": "passing"}],
            },
            {
                "Service": {"ID": "quote-svc-2", "Address": "quote-svc-2", "Port": 5002},
                "Checks": [{"Status": "passing"}],
            },
        ],
    )
    instances = discover_instances("localhost")
    assert len(instances) == 2
    assert instances[0] == {"id": "quote-svc-1", "address": "quote-svc-1", "port": 5001}
    assert instances[1] == {"id": "quote-svc-2", "address": "quote-svc-2", "port": 5002}


@patch("client.client.requests.get")
def test_discover_instances_returns_empty_when_none_healthy(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: [])
    instances = discover_instances("localhost")
    assert instances == []


@patch("client.client.requests.get")
def test_call_quote_service_returns_json(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"quote": "Be one.", "book": "Meditations, Book 10", "instance": "quote-svc-1"},
    )
    result = call_quote_service({"address": "quote-svc-1", "port": 5001})
    assert result["quote"] == "Be one."
    assert result["instance"] == "quote-svc-1"
