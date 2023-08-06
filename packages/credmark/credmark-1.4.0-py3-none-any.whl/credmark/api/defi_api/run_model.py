from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict

from ... import errors
from ...models.model_run_response import ModelRunResponse
from ...models.run_model_dto import RunModelDto
from ...types import Response


def _get_kwargs(*, json_body: RunModelDto, client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/model/run".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ModelRunResponse:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ModelRunResponse.from_dict(response.json())

        return response_201
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ModelRunResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, json_body: RunModelDto, client: "Credmark") -> Response[ModelRunResponse]:
    """Run model

     Runs a model and returns result object.

    Args:
        json_body (RunModelDto):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRunResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(*, json_body: RunModelDto, client: "Credmark") -> ModelRunResponse:
    """Run model

     Runs a model and returns result object.

    Args:
        json_body (RunModelDto):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRunResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(*, json_body: RunModelDto, client: "Credmark") -> Response[ModelRunResponse]:
    """Run model

     Runs a model and returns result object.

    Args:
        json_body (RunModelDto):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRunResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, json_body: RunModelDto, client: "Credmark") -> ModelRunResponse:
    """Run model

     Runs a model and returns result object.

    Args:
        json_body (RunModelDto):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelRunResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
