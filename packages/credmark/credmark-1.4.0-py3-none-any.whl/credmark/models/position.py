from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="Position")


@attr.s(auto_attribs=True)
class Position:
    """
    Attributes:
        token_address (str): Token address Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        balance (float): Token balance scaled to token decimals Example: 248367.58266143446.
    """

    token_address: str
    balance: float

    def to_dict(self) -> Dict[str, Any]:
        token_address = self.token_address
        balance = self.balance

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tokenAddress": token_address,
                "balance": balance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token_address = d.pop("tokenAddress")

        balance = d.pop("balance")

        position = cls(
            token_address=token_address,
            balance=balance,
        )

        return position
