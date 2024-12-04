from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass, asdict, field


class PaymentStatus(Enum):
    APPROVED = 1
    REFUSED = 2
    ERROR = 3

    @classmethod
    def from_value(cls, value):
        return cls(value=value)


@dataclass(slots=True)
class PaymentTypeEntity:
    id: int = field(default=None, repr=False, kw_only=True)
    name: str
    description: str
    created_at: datetime = field(default=datetime.now(), kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


@dataclass(slots=True)
class PaymentEntity:
    id: int = field(default=None, repr=False, kw_only=True)
    order_id: int
    amount: float
    type: PaymentTypeEntity
    status: PaymentStatus
    created_at: datetime = field(default=datetime.now(), kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)

    def as_dict(self) -> Dict:
        serialized = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        return serialized

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data
        data_copy["type"] = PaymentTypeEntity.from_dict(data=data["type"])
        data_copy["status"] = PaymentStatus(data["status"])
        return cls(**data_copy)


@dataclass(frozen=True)
class PaymentEntityFilter:
    order_id: Optional[int] = None
    status: Optional[str] = PaymentStatus.APPROVED.name
