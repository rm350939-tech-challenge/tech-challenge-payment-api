import os
from typing import Dict, List, Optional
from datetime import datetime

from domain.entities import (
    PaymentEntity,
    PaymentEntityFilter,
    PaymentStatus,
    PaymentTypeEntity,
)
from ports.repositories import (
    PaymentRepositoryInterface,
    PaymentTypeRepositoryInterface,
)

from playhouse.shortcuts import model_to_dict
from peewee import (
    PostgresqlDatabase,
    Model,
    CharField,
    DateTimeField,
    SmallIntegerField,
    IntegerField,
    TextField,
    DecimalField,
    ForeignKeyField,
)

db = PostgresqlDatabase(
    database=os.environ.get("DATABASE_NAME"),
    host=os.environ.get("DATABASE_HOST"),
    port=os.environ.get("DATABASE_PORT"),
    user=os.environ.get("DATABASE_USER"),
    password=os.environ.get("DATABASE_PASSWORD"),
)


class PaymentTypeModel(Model):
    name: str = CharField(max_length=80)
    description: str = TextField()
    created_at: datetime = DateTimeField()

    def model_to_dict(self) -> Dict:
        return model_to_dict(self)

    class Meta:
        database = db
        table_name = "payment_types"
        schema = os.environ.get("DATABASE_SCHEMA_NAME")


class PaymentModel(Model):
    order_id: int = IntegerField()
    amount: float = DecimalField()
    type: int = ForeignKeyField(PaymentTypeModel)
    status: int = SmallIntegerField()
    created_at: datetime = DateTimeField()

    def model_to_dict(self) -> Dict:
        return model_to_dict(self, backrefs=True)

    class Meta:
        database = db
        table_name = "payments"
        schema = os.environ.get("DATABASE_SCHEMA_NAME")


class PaymentRepository(PaymentRepositoryInterface):

    def create(self, payment_entity: PaymentEntity) -> PaymentEntity:
        payment = PaymentModel.create(
            order_id=payment_entity.order_id,
            type_id=payment_entity.type.id,
            amount=payment_entity.amount,
            status=payment_entity.status.value,
            created_at=payment_entity.created_at,
        )
        return PaymentEntity.from_dict(data=payment.model_to_dict())

    def list(self, filters: PaymentEntityFilter) -> List[PaymentEntity]:
        where = tuple()
        if filters.order_id:
            where += (PaymentModel.order_id == filters.order_id,)
        if filters.status:
            where += (PaymentModel.status == PaymentStatus[filters.status].value,)
        orders = (
            PaymentModel.select().where(*where)
            if len(where) > 0
            else PaymentModel.select()
        )
        return [PaymentEntity.from_dict(order.model_to_dict()) for order in orders]

    def get_by_id(self, payment_id: int) -> Optional[PaymentEntity] | None:
        payment = PaymentModel.get_or_none(id=payment_id)
        if not payment:
            return None
        return PaymentEntity.from_dict(payment.model_to_dict())

    def patch(self, payment_id: int, **fields) -> Optional[PaymentEntity] | None:
        payment = PaymentModel.get_or_none(id=payment_id)
        if not payment:
            return None
        for key, value in fields.items():
            if hasattr(PaymentEntity, key):
                setattr(payment, key, value)
        updated_payment = PaymentEntity.from_dict(payment.model_to_dict())
        payment.save()
        return updated_payment


class PaymentTypeRepository(PaymentTypeRepositoryInterface):

    def create(self, payment_type_entity: PaymentTypeEntity) -> PaymentTypeEntity:
        category = PaymentTypeModel.create(
            name=payment_type_entity.name,
            description=payment_type_entity.description,
            created_at=payment_type_entity.created_at,
        )
        return PaymentTypeEntity.from_dict(data=category.model_to_dict())

    def list(self) -> List[PaymentTypeEntity] | None:
        payment_types = PaymentTypeModel.select()
        if not payment_types:
            return None
        return [
            PaymentTypeEntity.from_dict(data=payment_type.model_to_dict())
            for payment_type in payment_types
        ]

    def get_by_id(self, payment_type_id: int) -> PaymentTypeEntity | None:
        payment = PaymentTypeModel.get_or_none(id=payment_type_id)
        if not payment:
            return None
        return PaymentTypeEntity.from_dict(payment.model_to_dict())
