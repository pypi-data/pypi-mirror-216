from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict

from ... import errors
from ...models.model_metadata import ModelMetadata
from ...types import Response


def _get_kwargs(slug: str, client: "Credmark") -> Dict[str, Any]:
    url = "{}/v1/models/{slug}".format(client.base_url, slug=slug)

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ModelMetadata:
    if response.status_code == HTTPStatus.OK:
        response_200 = ModelMetadata.from_dict(response.json())

        return response_200
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ModelMetadata]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(slug: str, client: "Credmark") -> Response[ModelMetadata]:
    """Get model metadata by slug

     Returns the metadata for the specified model.

    Args:
        slug (str):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelMetadata]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(slug: str, client: "Credmark") -> ModelMetadata:
    """Get model metadata by slug

     Returns the metadata for the specified model.

    Args:
        slug (str):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelMetadata]
    """

    return sync_detailed(
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(slug: str, client: "Credmark") -> Response[ModelMetadata]:
    """Get model metadata by slug

     Returns the metadata for the specified model.

    Args:
        slug (str):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelMetadata]
    """

    kwargs = _get_kwargs(
        slug=slug,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(slug: str, client: "Credmark") -> ModelMetadata:
    """Get model metadata by slug

     Returns the metadata for the specified model.

    Args:
        slug (str):

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ModelMetadata]
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
        )
    ).parsed
