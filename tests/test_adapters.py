import os
from unittest.mock import patch, MagicMock
from adapters.services import OrderServiceAdapter


def test_order_service_adapter_initialization():
    os.environ["ORDER_SERVICE_API"] = "http://mock-api.com"

    adapter = OrderServiceAdapter()

    assert adapter.order_service_api == "http://mock-api.com"


# Teste para o método update_status_order
@patch("requests.patch")
def test_update_status_order(mock_patch):
    order_id = 123
    status = "Shipped"
    mock_response = MagicMock()

    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "Shipped"}
    mock_patch.return_value = mock_response

    adapter = OrderServiceAdapter()
    adapter.order_service_api = "http://mock-api.com"

    response = adapter.update_status_order(order_id, status)

    mock_patch.assert_called_once_with(
        url="http://mock-api.com/api/v1/orders/123/status",
        data='{"status": "Shipped"}',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "Shipped"}


@patch("requests.patch")
def test_update_status_order_failure(mock_patch):
    order_id = 123
    status = "Failed"
    mock_response = MagicMock()

    mock_response.status_code = 500
    mock_patch.return_value = mock_response

    adapter = OrderServiceAdapter()
    adapter.order_service_api = "http://mock-api.com"

    response = adapter.update_status_order(order_id, status)

    mock_patch.assert_called_once_with(
        url="http://mock-api.com/api/v1/orders/123/status",
        data='{"status": "Failed"}',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 500
