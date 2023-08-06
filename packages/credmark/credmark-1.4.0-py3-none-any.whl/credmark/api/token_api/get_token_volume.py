from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Union

from ... import errors
from ...models.token_error_response import TokenErrorResponse
from ...models.token_volume_response import TokenVolumeResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    token_address: str,
    *,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/volume".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["scaled"] = scaled

    params["startBlockNumber"] = start_block_number

    params["endBlockNumber"] = end_block_number

    params["startTimestamp"] = start_timestamp

    params["endTimestamp"] = end_timestamp

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> TokenVolumeResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenVolumeResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = TokenErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[TokenVolumeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: int,
    token_address: str,
    *,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[TokenVolumeResponse]:
    """Get token volume

     Returns traded volume for a token over a period of blocks or time.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        scaled (Union[Unset, None, bool]): Scale volume by token decimals. Defaults to `true`.
            Default: True.
        start_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed.
        end_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed. Defaults to the latest block.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenVolumeResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: int,
    token_address: str,
    *,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> TokenVolumeResponse:
    """Get token volume

     Returns traded volume for a token over a period of blocks or time.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        scaled (Union[Unset, None, bool]): Scale volume by token decimals. Defaults to `true`.
            Default: True.
        start_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed.
        end_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed. Defaults to the latest block.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenVolumeResponse]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    token_address: str,
    *,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[TokenVolumeResponse]:
    """Get token volume

     Returns traded volume for a token over a period of blocks or time.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        scaled (Union[Unset, None, bool]): Scale volume by token decimals. Defaults to `true`.
            Default: True.
        start_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed.
        end_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed. Defaults to the latest block.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenVolumeResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        scaled=scaled,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    token_address: str,
    *,
    scaled: Union[Unset, None, bool] = True,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> TokenVolumeResponse:
    """Get token volume

     Returns traded volume for a token over a period of blocks or time.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        scaled (Union[Unset, None, bool]): Scale volume by token decimals. Defaults to `true`.
            Default: True.
        start_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed.
        end_block_number (Union[Unset, None, float]): Start block number of duration for which
            token volume will be computed. Defaults to the latest block.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenVolumeResponse]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
    ).parsed
