from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, List, Union, cast

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import List, Union, cast

from ... import errors
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    days: Union[Unset, None, float] = UNSET,
    group_by: Union[Unset, None, str] = UNSET,
    requester: Union[Unset, None, str] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/usage/requests".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["days"] = days

    params["groupBy"] = group_by

    params["requester"] = requester

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> List[Dict[str, Any]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[Dict[str, Any]], response.json())

        return response_200
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[List[Dict[str, Any]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    days: Union[Unset, None, float] = UNSET,
    group_by: Union[Unset, None, str] = UNSET,
    requester: Union[Unset, None, str] = UNSET,
    client: "Credmark",
) -> Response[List[Dict[str, Any]]]:
    """Model Request statistics

     Returns a list of daily model request statistics, either for a specific requester or for everyone.

    Args:
        days (Union[Unset, None, float]): Size of window in days [OPTIONAL]. Defaults to 90.
        group_by (Union[Unset, None, str]): Group results by "model", "requester-model",
            "requester" [OPTIONAL]. Only used if `requester` is not specified. Defaults to "model".
        requester (Union[Unset, None, str]): The NFT Id of the requester [OPTIONAL]

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    kwargs = _get_kwargs(
        client=client,
        days=days,
        group_by=group_by,
        requester=requester,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    days: Union[Unset, None, float] = UNSET,
    group_by: Union[Unset, None, str] = UNSET,
    requester: Union[Unset, None, str] = UNSET,
    client: "Credmark",
) -> List[Dict[str, Any]]:
    """Model Request statistics

     Returns a list of daily model request statistics, either for a specific requester or for everyone.

    Args:
        days (Union[Unset, None, float]): Size of window in days [OPTIONAL]. Defaults to 90.
        group_by (Union[Unset, None, str]): Group results by "model", "requester-model",
            "requester" [OPTIONAL]. Only used if `requester` is not specified. Defaults to "model".
        requester (Union[Unset, None, str]): The NFT Id of the requester [OPTIONAL]

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    return sync_detailed(
        client=client,
        days=days,
        group_by=group_by,
        requester=requester,
    ).parsed


async def asyncio_detailed(
    *,
    days: Union[Unset, None, float] = UNSET,
    group_by: Union[Unset, None, str] = UNSET,
    requester: Union[Unset, None, str] = UNSET,
    client: "Credmark",
) -> Response[List[Dict[str, Any]]]:
    """Model Request statistics

     Returns a list of daily model request statistics, either for a specific requester or for everyone.

    Args:
        days (Union[Unset, None, float]): Size of window in days [OPTIONAL]. Defaults to 90.
        group_by (Union[Unset, None, str]): Group results by "model", "requester-model",
            "requester" [OPTIONAL]. Only used if `requester` is not specified. Defaults to "model".
        requester (Union[Unset, None, str]): The NFT Id of the requester [OPTIONAL]

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    kwargs = _get_kwargs(
        client=client,
        days=days,
        group_by=group_by,
        requester=requester,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    days: Union[Unset, None, float] = UNSET,
    group_by: Union[Unset, None, str] = UNSET,
    requester: Union[Unset, None, str] = UNSET,
    client: "Credmark",
) -> List[Dict[str, Any]]:
    """Model Request statistics

     Returns a list of daily model request statistics, either for a specific requester or for everyone.

    Args:
        days (Union[Unset, None, float]): Size of window in days [OPTIONAL]. Defaults to 90.
        group_by (Union[Unset, None, str]): Group results by "model", "requester-model",
            "requester" [OPTIONAL]. Only used if `requester` is not specified. Defaults to "model".
        requester (Union[Unset, None, str]): The NFT Id of the requester [OPTIONAL]

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[Dict[str, Any]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
            group_by=group_by,
            requester=requester,
        )
    ).parsed
