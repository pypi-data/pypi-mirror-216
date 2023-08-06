# Utilities


Method | HTTP Request | Description
------------- | ------------- | -------------
[**check_health**](#check_health) | GET /health | 
[**get_daily_model_usage**](#get_daily_model_usage) | GET /v1/usage/requests | Returns a list of daily model request statistics, either for a specific requester or for everyone.
[**get_top_models**](#get_top_models) | GET /v1/usage/top | Returns a list of the top used models.
[**get_total_model_usage**](#get_total_model_usage) | GET /v1/usage/total | Returns a count of model runs.


# **check_health**

Healthcheck status



### Response Type
CheckHealthResponse200

# **get_daily_model_usage**

Model Request statistics

 Returns a list of daily model request statistics, either for a specific requester or for everyone.


### Parameters:
Name | Type | Description
------------ | ------------- | -------------
days | float | Size of window in days [OPTIONAL]. Defaults to 90.
group_by | str | Group results by "model", "requester-model", "requester" [OPTIONAL]. Only used if `requester` is not specified. Defaults to "model".
requester | str | The NFT Id of the requester [OPTIONAL]


### Response Type
List[Dict[str, Any]]

# **get_top_models**

Top Used Models

 Returns a list of the top used models.



### Response Type
List[Dict[str, Any]]

# **get_total_model_usage**

Total Model Usage

 Returns a count of model runs.



### Response Type
List[Dict[str, Any]]

