import pytest
from datetime import datetime
from domain.entities import PaymentEntity, PaymentStatus, PaymentTypeEntity
from adapters.dto import OutputPaymentDTO


@pytest.fixture
def payment_entity():
    payment_type = PaymentTypeEntity(
        id=1, name="Credit Card", description="Payment via credit card"
    )
    return PaymentEntity(
        id=1,
        order_id=123,
        amount=100.50,
        type=payment_type,
        status=PaymentStatus.APPROVED,
        created_at=datetime(2024, 12, 1, 10, 30, 0),
    )


def test_from_domain(payment_entity):
    dto = OutputPaymentDTO.from_domain(payment_entity)

    assert dto.id == payment_entity.id
    assert dto.order_id == payment_entity.order_id
    assert dto.amount == payment_entity.amount
    assert dto.type_id == payment_entity.type.id
    assert dto.status == payment_entity.status.name
    assert dto.created_at == payment_entity.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_to_dict(payment_entity):

    dto = OutputPaymentDTO.from_domain(payment_entity)

    dto_dict = dto.to_dict()

    assert dto_dict["id"] == payment_entity.id
    assert dto_dict["order_id"] == payment_entity.order_id
    assert dto_dict["amount"] == payment_entity.amount
    assert dto_dict["type_id"] == payment_entity.type.id
    assert dto_dict["status"] == payment_entity.status.name
    assert dto_dict["created_at"] == payment_entity.created_at.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    assert "none_field" not in dto_dict
