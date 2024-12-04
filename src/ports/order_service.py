from typing import Optional, List, Dict
from abc import ABC, abstractmethod

from domain.entities import PaymentEntity, PaymentEntityFilter, PaymentTypeEntity


class OrderServicePort(ABC):

    @abstractmethod
    def update_status_order(order_id: int, status: str):
        raise NotImplementedError
