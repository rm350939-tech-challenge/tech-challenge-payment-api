from http import HTTPStatus
from flask import Blueprint, request, jsonify

from adapters.dto import OutputPaymentDTO

from adapters.orm import PaymentRepository, PaymentTypeRepository
from domain.exceptions import EntityNotFoundException
from domain.services import PaymentService

service = PaymentService(
    payment_repository=PaymentRepository(),
    payment_type_repository=PaymentTypeRepository(),
)

payment_api = Blueprint("payment_api", __name__)


@payment_api.route("/payments", methods=["POST"], endpoint="register_payment")
def register_payment():
    try:
        payment = service.register_payment(**request.json)
        output = OutputPaymentDTO.from_domain(payment=payment).to_dict()
        return jsonify(output), HTTPStatus.CREATED
    except EntityNotFoundException as err:
        return jsonify({"error": err.message}), HTTPStatus.NOT_FOUND


@payment_api.route("/payments", methods=["GET"], endpoint="list_payment")
def list_payment():
    try:
        payments = service.list_all_payments(**request.args)
        return (
            jsonify(
                [
                    OutputPaymentDTO.from_domain(payment=payment).to_dict()
                    for payment in payments
                ]
            ),
            HTTPStatus.OK,
        )
    except EntityNotFoundException as err:
        return jsonify({"error": err.message}), HTTPStatus.NOT_FOUND
    except Exception as err:
        return jsonify({"error": err.args}), HTTPStatus.INTERNAL_SERVER_ERROR
