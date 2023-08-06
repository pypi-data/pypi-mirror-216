from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenValue")


@attr.s(auto_attribs=True)
class TokenValue:
    """
    Attributes:
        token_address (str): Token address Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        token_price (float): Token price in quoted currency. Example: 18990392.724937014.
        balance (float): Token balance scaled to token decimals Example: 248367.58266143446.
        value (float): Token value in quoted currency. Example: 18990392.724937014.
    """

    token_address: str
    token_price: float
    balance: float
    value: float

    def to_dict(self) -> Dict[str, Any]:
        token_address = self.token_address
        token_price = self.token_price
        balance = self.balance
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tokenAddress": token_address,
                "tokenPrice": token_price,
                "balance": balance,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token_address = d.pop("tokenAddress")

        token_price = d.pop("tokenPrice")

        balance = d.pop("balance")

        value = d.pop("value")

        token_value = cls(
            token_address=token_address,
            token_price=token_price,
            balance=balance,
            value=value,
        )

        return token_value
