from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenHolder")


@attr.s(auto_attribs=True)
class TokenHolder:
    """
    Attributes:
        address (str): Account address
        balance (float): Token balance Example: 248367.58266143446.
        value (float): Token value in quoted currency. Example: 18990392.724937014.
    """

    address: str
    balance: float
    value: float

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        balance = self.balance
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "address": address,
                "balance": balance,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        balance = d.pop("balance")

        value = d.pop("value")

        token_holder = cls(
            address=address,
            balance=balance,
            value=value,
        )

        return token_holder
