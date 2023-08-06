from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Union

from ... import errors
from ...models.get_cached_model_results_order import GetCachedModelResultsOrder
from ...models.model_runtime_stats_response import ModelRuntimeStatsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/model/results".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["slug"] = slug

    params["sort"] = sort

    json_order: Union[Unset, None, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value if order else None

    params["order"] = json_order

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ModelRuntimeStatsResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = ModelRuntimeStatsResponse.from_dict(response.json())

        return response_200
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ModelRuntimeStatsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str): Model slug
        sort (Union[Unset, None, str]): Field to sort results by: 'time', 'runtime'. Defaults to
            'time'.
        order (Union[Unset, None, GetCachedModelResultsOrder]): "asc" ascending order or "desc"
            descending order. Default is "desc".
        limit (Union[Unset, None, float]): Maximum number of results to return. Defaults to 100.
        offset (Union[Unset, None, float]): Offset index of results to return for pagination.
            Defaults to 0.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ModelRuntimeStatsResponse:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str): Model slug
        sort (Union[Unset, None, str]): Field to sort results by: 'time', 'runtime'. Defaults to
            'time'.
        order (Union[Unset, None, GetCachedModelResultsOrder]): "asc" ascending order or "desc"
            descending order. Default is "desc".
        limit (Union[Unset, None, float]): Maximum number of results to return. Defaults to 100.
        offset (Union[Unset, None, float]): Offset index of results to return for pagination.
            Defaults to 0.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return sync_detailed(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ModelRuntimeStatsResponse]:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str): Model slug
        sort (Union[Unset, None, str]): Field to sort results by: 'time', 'runtime'. Defaults to
            'time'.
        order (Union[Unset, None, GetCachedModelResultsOrder]): "asc" ascending order or "desc"
            descending order. Default is "desc".
        limit (Union[Unset, None, float]): Maximum number of results to return. Defaults to 100.
        offset (Union[Unset, None, float]): Offset index of results to return for pagination.
            Defaults to 0.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        slug=slug,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    slug: str,
    sort: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, GetCachedModelResultsOrder] = UNSET,
    limit: Union[Unset, None, float] = UNSET,
    offset: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ModelRuntimeStatsResponse:
    """Cached model results

     Returns cached run results for a slug.<p>This endpoint is for analyzing model runs. To run a model
    and get results, use `POST /v1/model/run`.

    Args:
        slug (str): Model slug
        sort (Union[Unset, None, str]): Field to sort results by: 'time', 'runtime'. Defaults to
            'time'.
        order (Union[Unset, None, GetCachedModelResultsOrder]): "asc" ascending order or "desc"
            descending order. Default is "desc".
        limit (Union[Unset, None, float]): Maximum number of results to return. Defaults to 100.
        offset (Union[Unset, None, float]): Offset index of results to return for pagination.
            Defaults to 0.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            slug=slug,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
        )
    ).parsed
