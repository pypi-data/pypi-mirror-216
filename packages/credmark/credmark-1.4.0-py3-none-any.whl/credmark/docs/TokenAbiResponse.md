# TokenAbiResponse


## Properties
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | Chain ID.
block_number | float | Block number.
block_timestamp | float | Block timestamp. Number of seconds since January 1, 1970.
token_address | str | Token address for the price.
abi | List[Dict[str, Any]] | Token ABI
is_transparent_proxy | bool | Whether the contract is using transparent proxy pattern.
proxy_implementation_address | Union[Unset, str] | Address of proxy contract's implementation. It is only set when the contract is implemented via proxy contract.

