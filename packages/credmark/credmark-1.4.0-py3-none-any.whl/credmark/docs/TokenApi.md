# Token API


Method | HTTP Request | Description
------------- | ------------- | -------------
[**get_token_metadata**](#get_token_metadata) | GET /v1/tokens/{chainId}/{tokenAddress} | Returns metadata for a token.
[**get_token_name**](#get_token_name) | GET /v1/tokens/{chainId}/{tokenAddress}/name | Returns name of a token.
[**get_token_symbol**](#get_token_symbol) | GET /v1/tokens/{chainId}/{tokenAddress}/symbol | Returns symbol of a token.
[**get_token_decimals**](#get_token_decimals) | GET /v1/tokens/{chainId}/{tokenAddress}/decimals | Returns decimals of a token.
[**get_token_total_supply**](#get_token_total_supply) | GET /v1/tokens/{chainId}/{tokenAddress}/total-supply | Returns total supply of a token.
[**get_token_total_supply_historical**](#get_token_total_supply_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/total-supply/historical | Returns historical total supply for a token.
[**get_token_logo**](#get_token_logo) | GET /v1/tokens/{chainId}/{tokenAddress}/logo | Returns logo of a token.
[**get_token_creation_block**](#get_token_creation_block) | GET /v1/tokens/{chainId}/{tokenAddress}/creation-block | Returns creation block number of a token.
[**get_token_abi**](#get_token_abi) | GET /v1/tokens/{chainId}/{tokenAddress}/abi | Returns ABI of a token.
[**get_token_price**](#get_token_price) | GET /v1/tokens/{chainId}/{tokenAddress}/price | Returns price data for a token.
[**get_token_price_historical**](#get_token_price_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/price/historical | Returns historical price data for a token.
[**get_token_balance**](#get_token_balance) | GET /v1/tokens/{chainId}/{tokenAddress}/balance | Returns token balance for an account.
[**get_token_balance_historical**](#get_token_balance_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/balance/historical | Returns historical token balance for an account.
[**get_token_volume**](#get_token_volume) | GET /v1/tokens/{chainId}/{tokenAddress}/volume | Returns traded volume for a token over a period of blocks or time.
[**get_token_volume_historical**](#get_token_volume_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/volume/historical | Returns traded volume for a token over a period of blocks or time divided by intervals.
[**get_token_holders**](#get_token_holders) | GET /v1/tokens/{chainId}/{tokenAddress}/holders | Returns holders of a token at a block or time.
[**get_token_holders_count**](#get_token_holders_count) | GET /v1/tokens/{chainId}/{tokenAddress}/holders/count | Returns total number of holders of a token at a block or time.
[**get_token_holders_count_historical**](#get_token_holders_count_historical) | GET /v1/tokens/{chainId}/{tokenAddress}/holders/count/historical | Returns historical total number of holders of a token at a block or time.


# **get_token_metadata**

Get token metadata

 Returns metadata for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the metadata. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenMetadataResponse

# **get_token_name**

Get token name

 Returns name of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the name. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenNameResponse

# **get_token_symbol**

Get token symbol

 Returns symbol of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the symbol. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenSymbolResponse

# **get_token_decimals**

Get token decimals

 Returns decimals of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the decimals. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenDecimalsResponse

# **get_token_total_supply**

Get token's total supply

 Returns total supply of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the total supply. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.
scaled | bool | Scale total supply by token decimals. Defaults to `true`.


### Response Type
TokenTotalSupplyResponse

# **get_token_total_supply_historical**

Get historical total supply

 Returns historical total supply for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
start_block_number | float | Start block number of the balance. Defaults to token's creation block.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.
scaled | bool | Scale total supply by token decimals. Defaults to `true`.


### Response Type
TokenTotalSupplyHistoricalResponse

# **get_token_logo**

Get token logo

 Returns logo of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the logo. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenLogoResponse

# **get_token_creation_block**

Get token creation block

 Returns creation block number of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
block_number | float | Block number of the token. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenCreationBlockResponse

# **get_token_abi**

Get token ABI

 Returns ABI of a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
block_number | float | Block number of the ABI. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenAbiResponse

# **get_token_price**

Get token price data

 Returns price data for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
block_number | float | Block number of the price quote. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.
src | GetTokenPriceSrc | (Optional) specify preferred source to be queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to price.quote model)


### Response Type
TokenPriceResponse

# **get_token_price_historical**

Get historical price

 Returns historical price data for a token.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
start_block_number | float | Start block number of the balance. Defaults to token's creation block.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
src | GetTokenPriceHistoricalSrc | (Optional) specify preferred source to be queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to price.quote model)


### Response Type
TokenPriceHistoricalResponse

# **get_token_balance**

Get token balance

 Returns token balance for an account.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Ethereum Mainnet<br/>`10` - Optimism<br/>`56` - BSC<br/>`137` - Polygon Mainnet<br/>`250` - Fantom Opera<br/>`42161` - Arbitrum One<br/>`43114` - Avalanche C-Chain
token_address | str | The address of the token requested.
account_address | str | The address of the account for which balance of the token will be fetched.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
scaled | bool | Scale balance by token decimals. Defaults to `true`.
block_number | float | Block number of the balance. Defaults to the latest block.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenBalanceResponse

# **get_token_balance_historical**

Get historical balance

 Returns historical token balance for an account.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
start_block_number | float | Start block number of the balance. Defaults to token's creation block.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.
account_address | str | The address of the account for which balance of the token will be fetched.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
scaled | bool | Scale balance by token decimals. Defaults to `true`.


### Response Type
TokenBalanceHistoricalResponse

# **get_token_volume**

Get token volume

 Returns traded volume for a token over a period of blocks or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
scaled | bool | Scale volume by token decimals. Defaults to `true`.
start_block_number | float | Start block number of duration for which token volume will be computed.
end_block_number | float | Start block number of duration for which token volume will be computed. Defaults to the latest block.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenVolumeResponse

# **get_token_volume_historical**

Get historical volume

 Returns traded volume for a token over a period of blocks or time divided by intervals.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
scaled | bool | Scale volume by token decimals. Defaults to `true`.
start_block_number | float | Start block number of duration for which token volume will be computed.
end_block_number | float | Start block number of duration for which token volume will be computed. Defaults to the latest block.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
block_interval | float | Number of blocks between each data point.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.


### Response Type
TokenVolumeHistoricalResponse

# **get_token_holders**

Get token holders

 Returns holders of a token at a block or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
page_size | float | The size of the returned page. Do not change this from page to page when using a cursor.
cursor | str | The cursor from the results of a previous page. Use empty string (or undefined/null) for first page.
quote_address | str | The address of the token/currency used as the currency of the returned price. Defaults to USD (address `0x0000000000000000000000000000000000000348`).
scaled | bool | Scale holders' balance by token decimals. Defaults to `true`.
block_number | float | Block number of the balance. Defaults to the latest block. Do not change this from page to page when using a cursor.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenHoldersResponse

# **get_token_holders_count**

Get total number of token holders

 Returns total number of holders of a token at a block or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
block_number | float | Block number of the balance. Defaults to the latest block. Do not change this from page to page when using a cursor.
timestamp | float | Timestamp of a block number can be specified instead of a block number. Finds a block at or before the number of seconds since January 1, 1970.


### Response Type
TokenHoldersCountResponse

# **get_token_holders_count_historical**

Get historical total number of token holders

 Returns historical total number of holders of a token at a block or time.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
chain_id | int | Chain identifier. This endpoint supports the following chains<br/><br/>`1` - Mainnet
token_address | str | The address of the token requested.
start_block_number | float | Start block number of the balance. Defaults to token's creation block.
end_block_number | float | End block number of the balance. Defaults to the latest block.
block_interval | float | Number of blocks between each data point.
start_timestamp | float | Start timestamp of a block number can be specified instead of start block number. Finds a block at or before the number of seconds since January 1, 1970.
end_timestamp | float | End timestamp of a block number can be specified instead of end block number. Finds a block at or before the number of seconds since January 1, 1970.
time_interval | float | Can be specified instead of blockInterval. Should be in seconds. Defaults to 86,400.


### Response Type
TokenHistoricalHoldersCountResponse

