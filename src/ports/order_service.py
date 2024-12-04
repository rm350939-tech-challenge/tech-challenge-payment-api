from abc import ABC, abstractmethod


class OrderServicePort(ABC):

    @abstractmethod
    def update_status_order(order_id: int, status: str):
        raise NotImplementedError
