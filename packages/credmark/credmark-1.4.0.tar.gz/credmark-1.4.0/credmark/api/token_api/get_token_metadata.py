from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Union

from ... import errors
from ...models.token_error_response import TokenErrorResponse
from ...models.token_metadata_response import TokenMetadataResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    token_address: str,
    *,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}".format(client.base_url, chainId=chain_id, tokenAddress=token_address)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["blockNumber"] = block_number

    params["timestamp"] = timestamp

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> TokenMetadataResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenMetadataResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = TokenErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[TokenMetadataResponse]:
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
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[TokenMetadataResponse]:
    """Get token metadata

     Returns metadata for a token.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Ethereum Mainnet
            `10` - Optimism
            `56` - BSC
            `137` - Polygon Mainnet
            `250` - Fantom Opera
            `42161` - Arbitrum One
            `43114` - Avalanche C-Chain
        token_address (str): The address of the token requested.
        block_number (Union[Unset, None, float]): Block number of the metadata. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenMetadataResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
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
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> TokenMetadataResponse:
    """Get token metadata

     Returns metadata for a token.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Ethereum Mainnet
            `10` - Optimism
            `56` - BSC
            `137` - Polygon Mainnet
            `250` - Fantom Opera
            `42161` - Arbitrum One
            `43114` - Avalanche C-Chain
        token_address (str): The address of the token requested.
        block_number (Union[Unset, None, float]): Block number of the metadata. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenMetadataResponse]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    token_address: str,
    *,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[TokenMetadataResponse]:
    """Get token metadata

     Returns metadata for a token.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Ethereum Mainnet
            `10` - Optimism
            `56` - BSC
            `137` - Polygon Mainnet
            `250` - Fantom Opera
            `42161` - Arbitrum One
            `43114` - Avalanche C-Chain
        token_address (str): The address of the token requested.
        block_number (Union[Unset, None, float]): Block number of the metadata. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenMetadataResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        block_number=block_number,
        timestamp=timestamp,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    token_address: str,
    *,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> TokenMetadataResponse:
    """Get token metadata

     Returns metadata for a token.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Ethereum Mainnet
            `10` - Optimism
            `56` - BSC
            `137` - Polygon Mainnet
            `250` - Fantom Opera
            `42161` - Arbitrum One
            `43114` - Avalanche C-Chain
        token_address (str): The address of the token requested.
        block_number (Union[Unset, None, float]): Block number of the metadata. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenMetadataResponse]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            block_number=block_number,
            timestamp=timestamp,
        )
    ).parsed
