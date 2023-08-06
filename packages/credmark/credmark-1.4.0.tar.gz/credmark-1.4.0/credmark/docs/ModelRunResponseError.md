# ModelRunResponseError


## Properties
Name | Type | Description
------------ | ------------- | -------------
type | str | Short identifying name for type of error
message | str | A descriptive message about the error
code | str | A short string, values to specific to the error type
permanent | bool | If true the error is considered deterministically permanent, for example a requested item does not exist on the blockchain within the context of a particular block.
stack | List['ModelCallStackEntry'] | None
detail | Optional[Dict[str, Any]] | An object or null. Some errors may have a detail object containing error-specific data.

