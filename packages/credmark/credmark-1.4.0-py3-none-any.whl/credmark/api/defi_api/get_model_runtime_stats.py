from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict

from ... import errors
from ...models.model_runtime_stats_response import ModelRuntimeStatsResponse
from ...types import Response


def _get_kwargs(client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/model/runtime-stats".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
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


def sync_detailed(client: "Credmark") -> Response[ModelRuntimeStatsResponse]:
    """Model runtime stats

     Returns runtime stats for all models.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(client: "Credmark") -> ModelRuntimeStatsResponse:
    """Model runtime stats

     Returns runtime stats for all models.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(client: "Credmark") -> Response[ModelRuntimeStatsResponse]:
    """Model runtime stats

     Returns runtime stats for all models.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(client: "Credmark") -> ModelRuntimeStatsResponse:
    """Model runtime stats

     Returns runtime stats for all models.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRuntimeStatsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
