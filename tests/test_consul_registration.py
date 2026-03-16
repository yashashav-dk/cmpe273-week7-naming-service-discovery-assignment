import json
from unittest.mock import patch, MagicMock
from quote_service.consul_registration import register_service, deregister_service


@patch("quote_service.consul_registration.requests.put")
def test_register_service_sends_correct_payload(mock_put):
    mock_put.return_value = MagicMock(status_code=200)
    register_service(
        consul_host="localhost",
        service_name="quote-service",
        instance_name="quote-svc-1",
        host="localhost",
        port=5001,
    )
    mock_put.assert_called_once()
    call_args = mock_put.call_args
    url = call_args[0][0]
    assert "/v1/agent/service/register" in url
    payload = json.loads(call_args[1]["data"])
    assert payload["Name"] == "quote-service"
    assert payload["ID"] == "quote-svc-1"
    assert payload["Port"] == 5001
    assert payload["Check"]["HTTP"] == "http://localhost:5001/health"


@patch("quote_service.consul_registration.requests.put")
def test_deregister_service_calls_correct_url(mock_put):
    mock_put.return_value = MagicMock(status_code=200)
    deregister_service(consul_host="localhost", instance_name="quote-svc-1")
    mock_put.assert_called_once()
    url = mock_put.call_args[0][0]
    assert "/v1/agent/service/deregister/quote-svc-1" in url


@patch("quote_service.consul_registration.time.sleep")
@patch("quote_service.consul_registration.requests.put")
def test_register_retries_on_failure(mock_put, mock_sleep):
    mock_put.side_effect = [ConnectionError, ConnectionError, MagicMock(status_code=200)]
    register_service(
        consul_host="localhost",
        service_name="quote-service",
        instance_name="quote-svc-1",
        host="localhost",
        port=5001,
    )
    assert mock_put.call_count == 3
    assert mock_sleep.call_count == 2
