# TokenHoldersResponse


## Properties
Name | Type | Description
------------ | ------------- | -------------
chain_id | float | Chain ID.
block_number | float | Block number.
block_timestamp | float | Block timestamp. Number of seconds since January 1, 1970.
token_address | str | Token address for the price.
scaled | bool | If the holders' balance is scaled by token decimals.
quote_address | str | Quote address is the token/currency of the price units.
data | List['TokenHolder'] | Paginated list of holders
total | float | Total number of holders
cursor | Union[Unset, str] | Cursor to fetch the next page

