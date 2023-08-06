# ModelMetadata


## Properties
Name | Type | Description
------------ | ------------- | -------------
slug | str | Short identifying name for the model
tags | List[str] | A list of tag strings for the model
display_name | Union[Unset, str] | Name of the model
description | Union[Unset, str] | A short description of the model
latest_version | Union[Unset, str] | Latest version of the model
developer | Union[Unset, str] | Name of the developer
category | Union[Unset, str] | The category of the model
subcategory | Union[Unset, str] | The subcategory of the model
attributes | Union[Unset, Dict[str, Any]] | Attributes for the model
input | Union[Unset, Dict[str, Any]] | Model input JSON schema
output | Union[Unset, Dict[str, Any]] | Model output JSON schema
error | Union[Unset, Dict[str, Any]] | Model error JSON schema
client | Union[Unset, str] | Client owner of the model
cmf_version | Union[Unset, str] | The version of the credmark model framework used in the latest deployment

