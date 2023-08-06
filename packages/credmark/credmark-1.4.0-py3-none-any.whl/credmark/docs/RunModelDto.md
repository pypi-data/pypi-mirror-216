# RunModelDto


## Properties
Name | Type | Description
------------ | ------------- | -------------
slug | str | slug of the model to run
chain_id | int | chainId number, for example 1 for mainnet
block_number | Union[RunModelDtoBlockNumberType1, int] | BlockNumber is a number, a number as string, 'latest' or 'earliest'
input | Dict[str, Any] | Model input data
version | Union[Unset, str] | Typically not required but you may specify version of the model to run

