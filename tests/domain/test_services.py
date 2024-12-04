import pytest
from unittest.mock import MagicMock
from domain.entities import PaymentEntity, PaymentStatus
from domain.exceptions import EntityNotFoundException
from domain.services import PaymentService


@pytest.fixture
def mock_payment_repository():
    return MagicMock()


@pytest.fixture
def mock_payment_type_repository():
    return MagicMock()


@pytest.fixture
def mock_order_service():
    return MagicMock()


@pytest.fixture
def payment_service(
    mock_payment_repository, mock_payment_type_repository, mock_order_service
):
    return PaymentService(
        payment_repository=mock_payment_repository,
        payment_type_repository=mock_payment_type_repository,
        order_service=mock_order_service,
    )


def test_register_payment_success(
    payment_service, mock_payment_repository, mock_payment_type_repository
):
    # Preparando os dados
    input_data = {"order_id": 123, "amount": 250.75, "type_id": 1}

    mock_payment_type_repository.get_by_id.return_value = MagicMock(
        id=1, name="Credit Card"
    )

    mock_payment_repository.create.return_value = PaymentEntity(
        order_id=123,
        amount=250.75,
        type=MagicMock(id=1, name="Credit Card"),
        status=PaymentStatus.APPROVED,
    )

    result = payment_service.register_payment(**input_data)

    assert result.order_id == 123
    assert result.amount == 250.75
    assert result.status == PaymentStatus.APPROVED
    mock_payment_repository.create.assert_called_once()


def test_register_payment_type_not_found(
    payment_service, mock_payment_repository, mock_payment_type_repository
):
    input_data = {
        "order_id": 123,
        "amount": 250.75,
        "type_id": 999,
    }

    mock_payment_type_repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundException, match="Payment type not found."):
        payment_service.register_payment(**input_data)


def test_list_all_payments_success(payment_service, mock_payment_repository):

    filters = {"order_id": 123, "status": PaymentStatus.APPROVED.name}

    mock_payment_repository.list.return_value = [
        MagicMock(order_id=123, amount=250.75, status=PaymentStatus.APPROVED)
    ]

    result = payment_service.list_all_payments(**filters)

    assert len(result) > 0
    assert result[0].order_id == 123
    assert result[0].status == PaymentStatus.APPROVED
    mock_payment_repository.list.assert_called_once()


def test_list_all_payments_not_found(payment_service, mock_payment_repository):

    filters = {"order_id": 123, "status": PaymentStatus.APPROVED.name}

    mock_payment_repository.list.return_value = []

    with pytest.raises(EntityNotFoundException, match="No payments found."):
        payment_service.list_all_payments(**filters)


def test_update_status_payment_success(payment_service, mock_payment_repository):
    payment = MagicMock(
        id=1, order_id=123, amount=250.75, status=PaymentStatus.APPROVED
    )
    mock_payment_repository.get_by_id.return_value = payment

    mock_payment_repository.patch.return_value = MagicMock(
        id=1, order_id=123, amount=250.75, status=PaymentStatus.REFUSED
    )

    result = payment_service.update_status_payment(
        payment_id=1, status=PaymentStatus.REFUSED.name
    )

    assert result.status == PaymentStatus.REFUSED
    mock_payment_repository.patch.assert_called_once()


def test_update_status_payment_not_found(payment_service, mock_payment_repository):
    mock_payment_repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundException, match="No payments found."):
        payment_service.update_status_payment(
            payment_id=1, status=PaymentStatus.REFUSED.name
        )
