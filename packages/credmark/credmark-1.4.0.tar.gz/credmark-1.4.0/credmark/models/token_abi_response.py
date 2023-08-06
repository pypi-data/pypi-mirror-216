from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenAbiResponse")


@attr.s(auto_attribs=True)
class TokenAbiResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        token_address (str): Token address for the price. Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        abi (List[Dict[str, Any]]): Token ABI Example: [{'name': 'AdminChanged', 'type': 'event', 'inputs': [{'name':
            'previousAdmin', 'type': 'address', 'indexed': False, 'internalType': 'address'}, {'name': 'newAdmin', 'type':
            'address', 'indexed': False, 'internalType': 'address'}], 'anonymous': False}, {'name': 'Upgraded', 'type':
            'event', 'inputs': [{'name': 'implementation', 'type': 'address', 'indexed': True, 'internalType': 'address'}],
            'anonymous': False}, {'type': 'fallback', 'stateMutability': 'payable'}, {'name': 'admin', 'type': 'function',
            'inputs': [], 'outputs': [{'name': '', 'type': 'address', 'internalType': 'address'}], 'stateMutability':
            'nonpayable'}, {'name': 'changeAdmin', 'type': 'function', 'inputs': [{'name': 'newAdmin', 'type': 'address',
            'internalType': 'address'}], 'outputs': [], 'stateMutability': 'nonpayable'}, {'name': 'implementation', 'type':
            'function', 'inputs': [], 'outputs': [{'name': '', 'type': 'address', 'internalType': 'address'}],
            'stateMutability': 'nonpayable'}, {'name': 'initialize', 'type': 'function', 'inputs': [{'name': '_logic',
            'type': 'address', 'internalType': 'address'}, {'name': '_admin', 'type': 'address', 'internalType': 'address'},
            {'name': '_data', 'type': 'bytes', 'internalType': 'bytes'}], 'outputs': [], 'stateMutability': 'payable'},
            {'name': 'initialize', 'type': 'function', 'inputs': [{'name': '_logic', 'type': 'address', 'internalType':
            'address'}, {'name': '_data', 'type': 'bytes', 'internalType': 'bytes'}], 'outputs': [], 'stateMutability':
            'payable'}, {'name': 'upgradeTo', 'type': 'function', 'inputs': [{'name': 'newImplementation', 'type':
            'address', 'internalType': 'address'}], 'outputs': [], 'stateMutability': 'nonpayable'}, {'name':
            'upgradeToAndCall', 'type': 'function', 'inputs': [{'name': 'newImplementation', 'type': 'address',
            'internalType': 'address'}, {'name': 'data', 'type': 'bytes', 'internalType': 'bytes'}], 'outputs': [],
            'stateMutability': 'payable'}].
        is_transparent_proxy (bool): Whether the contract is using transparent proxy pattern. Example: True.
        proxy_implementation_address (Union[Unset, str]): Address of proxy contract's implementation. It is only set
            when the contract is implemented via proxy contract. Example: 0xc13eac3b4f9eed480045113b7af00f7b5655ece8.
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    token_address: str
    abi: List[Dict[str, Any]]
    is_transparent_proxy: bool
    proxy_implementation_address: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        token_address = self.token_address
        abi = self.abi

        is_transparent_proxy = self.is_transparent_proxy
        proxy_implementation_address = self.proxy_implementation_address

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "tokenAddress": token_address,
                "abi": abi,
                "isTransparentProxy": is_transparent_proxy,
            }
        )
        if proxy_implementation_address is not UNSET:
            field_dict["proxyImplementationAddress"] = proxy_implementation_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        token_address = d.pop("tokenAddress")

        abi = cast(List[Dict[str, Any]], d.pop("abi"))

        is_transparent_proxy = d.pop("isTransparentProxy")

        proxy_implementation_address = d.pop("proxyImplementationAddress", UNSET)

        token_abi_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            token_address=token_address,
            abi=abi,
            is_transparent_proxy=is_transparent_proxy,
            proxy_implementation_address=proxy_implementation_address,
        )

        return token_abi_response
