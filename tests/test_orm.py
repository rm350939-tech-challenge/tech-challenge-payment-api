import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from domain.entities import (
    PaymentEntity,
    PaymentEntityFilter,
    PaymentStatus,
    PaymentTypeEntity,
)
from adapters.orm import PaymentRepository, PaymentTypeRepository


@pytest.fixture
def mock_db(mocker):
    mocker.patch("peewee.Model.save", return_value=None)
    mocker.patch("peewee.Model.create", return_value=None)
    mocker.patch("peewee.Model.get_or_none", return_value=None)
    mocker.patch("peewee.Model.select", return_value=[])


@pytest.fixture
def mock_payment_entity():
    return PaymentEntity(
        id=1,
        order_id=123,
        type={"id": 1, "name": "Credit Card", "description": "Description"},
        amount=100.0,
        status=PaymentStatus.APPROVED,
        created_at=datetime.now(),
    )


@pytest.fixture
def payment_repository():
    return PaymentRepository()


def test_list_payments(mock_db, payment_repository, mock_payment_entity):
    mock_query_set = MagicMock()
    mock_query_set.where.return_value = [
        MagicMock(model_to_dict=lambda: mock_payment_entity.as_dict())
    ]

    with patch("adapters.orm.PaymentModel.select", return_value=mock_query_set):
        filters = PaymentEntityFilter(order_id=123, status="APPROVED")
        payments = payment_repository.list(filters)
        assert len(payments) == 1
        assert payments[0].order_id == mock_payment_entity.order_id


def test_get_payment_by_id(mock_db, payment_repository, mock_payment_entity):
    mock_payment = MagicMock(model_to_dict=lambda: mock_payment_entity.as_dict())

    with patch("adapters.orm.PaymentModel.get_or_none", return_value=mock_payment):
        payment = payment_repository.get_by_id(1)
        assert payment is not None
        assert payment.order_id == mock_payment_entity.order_id


def test_patch_payment(mock_db, payment_repository, mock_payment_entity):
    updated_fields = {"amount": 200.0}
    mock_payment = MagicMock()
    mock_payment.model_to_dict = lambda: {
        **mock_payment_entity.as_dict(),
        **updated_fields,
    }

    with patch("adapters.orm.PaymentModel.get_or_none", return_value=mock_payment):
        payment = payment_repository.patch(1, amount=200.0)
        assert payment is not None
        assert payment.amount == 200.0


@pytest.fixture
def mock_payment_type_entity():
    entity = PaymentTypeEntity(
        id=1,
        name="Credit Card",
        description="Description",
        created_at=datetime.now(),
    )

    return entity


@pytest.fixture
def payment_type_repository():
    return PaymentTypeRepository()
