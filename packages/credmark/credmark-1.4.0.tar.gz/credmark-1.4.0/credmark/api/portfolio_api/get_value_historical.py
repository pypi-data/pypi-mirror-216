from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, List, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, List, Union

from ... import errors
from ...models.portfolio_error_response import PortfolioErrorResponse
from ...models.value_historical_response import ValueHistoricalResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/portfolio/{chainId}/{accounts}/value/historical".format(
        client.base_url, chainId=chain_id, accounts=",".join(accounts)
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_tokens: Union[Unset, None, List[str]] = UNSET
    if not isinstance(tokens, Unset):
        if tokens is None:
            json_tokens = None
        else:
            json_tokens = tokens

    params["tokens"] = json_tokens

    params["quoteAddress"] = quote_address

    params["includePositions"] = include_positions

    params["startBlockNumber"] = start_block_number

    params["endBlockNumber"] = end_block_number

    params["blockInterval"] = block_interval

    params["startTimestamp"] = start_timestamp

    params["endTimestamp"] = end_timestamp

    params["timeInterval"] = time_interval

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ValueHistoricalResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = ValueHistoricalResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PortfolioErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ValueHistoricalResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ValueHistoricalResponse]:
    """Get accounts' historical value

     Returns portfolio value for a list of accounts over a series of blocks.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        accounts (List[str]): Comma separated list of account addresses
        tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
            tokens are provided return positions for all tokens with non-zero balances.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        include_positions (Union[Unset, None, bool]): Set `true` to include positions. Defaults to
            `false`.
        start_block_number (Union[Unset, None, float]): Start block number. Required.
        end_block_number (Union[Unset, None, float]): End block number of the balance. Defaults to
            the latest block.
        block_interval (Union[Unset, None, float]): Number of blocks between each data point.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
            Should be in seconds. Defaults to 86,400.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueHistoricalResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ValueHistoricalResponse:
    """Get accounts' historical value

     Returns portfolio value for a list of accounts over a series of blocks.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        accounts (List[str]): Comma separated list of account addresses
        tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
            tokens are provided return positions for all tokens with non-zero balances.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        include_positions (Union[Unset, None, bool]): Set `true` to include positions. Defaults to
            `false`.
        start_block_number (Union[Unset, None, float]): Start block number. Required.
        end_block_number (Union[Unset, None, float]): End block number of the balance. Defaults to
            the latest block.
        block_interval (Union[Unset, None, float]): Number of blocks between each data point.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
            Should be in seconds. Defaults to 86,400.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueHistoricalResponse]
    """

    return sync_detailed(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ValueHistoricalResponse]:
    """Get accounts' historical value

     Returns portfolio value for a list of accounts over a series of blocks.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        accounts (List[str]): Comma separated list of account addresses
        tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
            tokens are provided return positions for all tokens with non-zero balances.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        include_positions (Union[Unset, None, bool]): Set `true` to include positions. Defaults to
            `false`.
        start_block_number (Union[Unset, None, float]): Start block number. Required.
        end_block_number (Union[Unset, None, float]): End block number of the balance. Defaults to
            the latest block.
        block_interval (Union[Unset, None, float]): Number of blocks between each data point.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
            Should be in seconds. Defaults to 86,400.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueHistoricalResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ValueHistoricalResponse:
    """Get accounts' historical value

     Returns portfolio value for a list of accounts over a series of blocks.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        accounts (List[str]): Comma separated list of account addresses
        tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
            tokens are provided return positions for all tokens with non-zero balances.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        include_positions (Union[Unset, None, bool]): Set `true` to include positions. Defaults to
            `false`.
        start_block_number (Union[Unset, None, float]): Start block number. Required.
        end_block_number (Union[Unset, None, float]): End block number of the balance. Defaults to
            the latest block.
        block_interval (Union[Unset, None, float]): Number of blocks between each data point.
        start_timestamp (Union[Unset, None, float]): Start timestamp of a block number can be
            specified instead of start block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        end_timestamp (Union[Unset, None, float]): End timestamp of a block number can be
            specified instead of end block number. Finds a block at or before the number of seconds
            since January 1, 1970.
        time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
            Should be in seconds. Defaults to 86,400.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueHistoricalResponse]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            accounts=accounts,
            client=client,
            tokens=tokens,
            quote_address=quote_address,
            include_positions=include_positions,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )
    ).parsed
