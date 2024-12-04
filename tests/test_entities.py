import pytest
from datetime import datetime
from domain.entities import (
    PaymentStatus,
    PaymentTypeEntity,
    PaymentEntity,
    PaymentEntityFilter,
)


def test_payment_status_from_value():
    assert PaymentStatus.from_value(1) == PaymentStatus.APPROVED
    assert PaymentStatus.from_value(2) == PaymentStatus.REFUSED
    assert PaymentStatus.from_value(3) == PaymentStatus.ERROR


def test_payment_status_invalid_value():
    with pytest.raises(ValueError):
        PaymentStatus.from_value(99)


def test_payment_type_entity_from_dict():
    data = {
        "name": "Credit Card",
        "description": "Payment via credit card",
    }
    entity = PaymentTypeEntity.from_dict(data)
    assert entity.name == "Credit Card"
    assert entity.description == "Payment via credit card"
    assert isinstance(entity.created_at, datetime)


def test_payment_entity_from_dict():
    data = {
        "order_id": 123,
        "amount": 250.75,
        "type": {"name": "Credit Card", "description": "Payment via credit card"},
        "status": 1,
    }
    entity = PaymentEntity.from_dict(data)
    assert entity.order_id == 123
    assert entity.amount == 250.75
    assert entity.type.name == "Credit Card"
    assert entity.status == PaymentStatus.APPROVED
    assert isinstance(entity.created_at, datetime)


def test_payment_entity_as_dict():
    payment_type = PaymentTypeEntity(
        name="Debit Card", description="Payment via debit card"
    )
    payment_entity = PaymentEntity(
        order_id=124, amount=150.50, type=payment_type, status=PaymentStatus.REFUSED
    )
    serialized = payment_entity.as_dict()
    assert "order_id" in serialized
    assert "amount" in serialized
    assert "status" in serialized
    assert "type" in serialized
    assert serialized["status"] == PaymentStatus.REFUSED
    assert serialized["type"]["name"] == "Debit Card"
    assert "created_at" in serialized


def test_payment_entity_filter_default_values():
    filter = PaymentEntityFilter()
    assert filter.order_id is None
    assert filter.status == PaymentStatus.APPROVED.name


def test_payment_entity_filter_with_values():
    filter = PaymentEntityFilter(order_id=123, status=PaymentStatus.REFUSED.name)
    assert filter.order_id == 123
    assert filter.status == PaymentStatus.REFUSED.name
