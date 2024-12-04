from typing import Optional, List
from abc import ABC, abstractmethod

from domain.entities import PaymentEntity, PaymentEntityFilter, PaymentTypeEntity


class PaymentRepositoryInterface(ABC):

    @abstractmethod
    def create(self, payment_entity: PaymentEntity) -> Optional[PaymentEntity]:
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: PaymentEntityFilter) -> List[PaymentEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Optional[PaymentEntity] | None:
        raise NotImplementedError

    @abstractmethod
    def patch(self, payment_id: int, **fields) -> Optional[PaymentEntity]:
        raise NotImplementedError


class PaymentTypeRepositoryInterface(ABC):

    @abstractmethod
    def create(
        self, payment_type_entity: PaymentTypeEntity
    ) -> Optional[PaymentTypeEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_type_id: int) -> Optional[PaymentTypeEntity] | None:
        raise NotImplementedError
