# Portfolio API


Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_positions**](#get_positions) | GET /v1/portfolio/{chainId}/{accounts}/positions | Returns positions for a list of accounts.
[**get_positions_historical**](#get_positions_historical) | GET /v1/portfolio/{chainId}/{accounts}/positions/historical | Returns positions for a list of accounts over a series of blocks.
[**get_value**](#get_value) | GET /v1/portfolio/{chainId}/{accounts}/value | Returns value of portfolio for a list of accounts.
[**get_value_historical**](#get_value_historical) | GET /v1/portfolio/{chainId}/{accounts}/value/historical | Returns portfolio value for a list of accounts over a series of blocks.
[**get_returns**](#get_returns) | GET /v1/portfolio/{chainId}/{accounts}/returns | Returns PnL of portfolio for a list of accounts.


# **get_positions**

Get accounts' positions

 Returns positions for a list of accounts.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
accounts | [List[str]](List[str]) | Comma separated list of account addresses
tokens | [List[str]](List[str]) | Comma separated list of token addresses. If no tokens are provided return positions for all tokens with non-zero balances.
block_number | float | Block number of the portfolio. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
PositionsResponse

# **get_positions_historical**

Get accounts' historical positions

 Returns positions for a list of accounts over a series of blocks.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
accounts | [List[str]](List[str]) | Comma separated list of account addresses
start_block_number | float | Start block number. Required.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.
tokens | [List[str]](List[str]) | Comma separated list of token addresses. If no tokens are provided return positions for all tokens with non-zero balances.


### Response Type
PositionsHistoricalResponse

# **get_value**

Get accounts' value

 Returns value of portfolio for a list of accounts.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
accounts | [List[str]](List[str]) | Comma separated list of account addresses
tokens | [List[str]](List[str]) | Comma separated list of token addresses. If no tokens are provided return positions for all tokens with non-zero balances.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
include_positions | bool | Set `true` to include positions. Defaults to `false`.
block_number | float | Block number of the portfolio. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
ValueResponse

# **get_value_historical**

Get accounts' historical value

 Returns portfolio value for a list of accounts over a series of blocks.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
accounts | [List[str]](List[str]) | Comma separated list of account addresses
tokens | [List[str]](List[str]) | Comma separated list of token addresses. If no tokens are provided return positions for all tokens with non-zero balances.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
include_positions | bool | Set `true` to include positions. Defaults to `false`.
start_block_number | float | Start block number. Required.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.


### Response Type
ValueHistoricalResponse

# **get_returns**

Get accounts' token returns

 Returns PnL of portfolio for a list of accounts.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
accounts | [List[str]](List[str]) | Comma separated list of account addresses
quote_address | str | The address of the token/currency used as the currency for price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
block_number | float | Block number of the portfolio. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
ReturnsResponse

