# DeFi API


Method | HTTP Request | Description
------------- | ------------- | -------------
[**list_models**](#list_models) | GET /v1/models | Returns a list of metadata for available models.
[**get_model_by_slug**](#get_model_by_slug) | GET /v1/models/{slug} | Returns the metadata for the specified model.
[**get_model_deployments_by_slug**](#get_model_deployments_by_slug) | GET /v1/models/{slug}/deployments | Returns the deployments for a model.
[**get_model_runtime_stats**](#get_model_runtime_stats) | GET /v1/model/runtime-stats | Returns runtime stats for all models.
[**get_cached_model_results**](#get_cached_model_results) | GET /v1/model/results | Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model and get results, use `POST /v1/model/run`.
[**run_model**](#run_model) | POST /v1/model/run | Runs a model and returns result object.


# **list_models**

List metadata for available models

 Returns a list of metadata for available models.



### Response Type
List['ModelMetadata']

# **get_model_by_slug**

Get model metadata by slug

 Returns the metadata for the specified model.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
slug | str | None


### Response Type
ModelMetadata

# **get_model_deployments_by_slug**

Get model deployments of a model by slug

 Returns the deployments for a model.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
slug | str | None


### Response Type
List['ModelDeployment']

# **get_model_runtime_stats**

Model runtime stats

 Returns runtime stats for all models.



### Response Type
ModelRuntimeStatsResponse

# **get_cached_model_results**

Cached model results

 Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
and get results, use `POST /v1/model/run`.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
slug | str | Model slug
sort | str | Field to sort results by: 'time', 'runtime'. Defaults to 'time'.
order | GetCachedModelResultsOrder | "asc" ascending order or "desc" descending order. Default is "desc".
limit | float | Maximum number of results to return. Defaults to 100.
offset | float | Offset index of results to return for pagination. Defaults to 0.


### Response Type
ModelRuntimeStatsResponse

# **run_model**

Run model

 Runs a model and returns result object.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
json_body | [RunModelDto](RunModelDto) | 


### Response Type
ModelRunResponse

