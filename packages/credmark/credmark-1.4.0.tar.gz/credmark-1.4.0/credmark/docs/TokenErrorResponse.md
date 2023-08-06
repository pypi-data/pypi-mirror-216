# TokenErrorResponse


## Properties
Name | Type | Description
------------ | ------------- | -------------
status_code | float | If an error response (non-200 status code), the status code will be set.
error | str | If an error response (non-200 status code), the error will be set with a short string for the code.
message | Union[List[str], str] | If an error response (non-200 status code), the message will be set with an error message. It can either be a string or a list of strings.

