from typing import List
from domain.entities import PaymentEntity, PaymentEntityFilter, PaymentStatus
from domain.exceptions import EntityNotFoundException

from ports.order_service import OrderServicePort
from ports.repositories import (
    PaymentRepositoryInterface,
    PaymentTypeRepositoryInterface,
)


class PaymentService:

    def __init__(
        self,
        payment_repository: PaymentRepositoryInterface,
        payment_type_repository: PaymentTypeRepositoryInterface,
        order_service: OrderServicePort,
    ) -> None:
        self._payment_repository = payment_repository
        self._payment_type_repository = payment_type_repository
        self._order_service = order_service

    def register_payment(self, **input_data) -> PaymentEntity:
        order_id = input_data.get("order_id")
        order_amount = input_data.get("amount")
        type_id = input_data.get("type_id")

        payment_type = self._payment_type_repository.get_by_id(payment_type_id=type_id)
        if not payment_type:
            raise EntityNotFoundException("Payment type not found.")

        payment = PaymentEntity(
            order_id=order_id,
            amount=order_amount,
            type=payment_type,
            status=PaymentStatus.APPROVED,
        )

        self._order_service.update_status_order(order_id, "RECEIVED")

        return self._payment_repository.create(payment_entity=payment)

    def list_all_payments(self, **filters) -> List[PaymentEntity]:
        payment_filters = PaymentEntityFilter(
            order_id=filters.get("order_id"), status=filters.get("status")
        )

        payments = self._payment_repository.list(filters=payment_filters)
        if not payments:
            raise EntityNotFoundException("No payments found.")

        return payments

    def update_status_payment(self, payment_id: int, status: str) -> PaymentEntity:
        payment = self._payment_repository.get_by_id(payment_id=payment_id)

        if not payment:
            raise EntityNotFoundException("No payments found.")

        updated_payment = self._payment_repository.patch(
            payment_id=payment_id, status=status
        )

        return updated_payment
