import pytest
from flask import Flask
from http import HTTPStatus
from unittest.mock import patch
from domain.exceptions import EntityNotFoundException

from domain.services import PaymentService
from adapters.http import payment_api


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(payment_api, url_prefix="/api/v1")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_payment_service():
    with patch.object(PaymentService, "register_payment") as mock_service:
        yield mock_service


def test_register_payment_entity_not_found(client, mock_payment_service):
    payment_data = {
        "order_id": 999,
        "amount": 100.00,
        "type_id": 2,
        "status": "PENDING",
        "created_at": "2024-12-03T12:00:00",
    }

    mock_payment_service.side_effect = EntityNotFoundException("Payment type not found")

    response = client.post("/api/v1/payments", json=payment_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    response_json = response.get_json()
    assert response_json["error"] == "Payment type not found"
