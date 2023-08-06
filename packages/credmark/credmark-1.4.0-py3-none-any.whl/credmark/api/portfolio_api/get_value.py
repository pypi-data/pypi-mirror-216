from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, List, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, List, Union

from ... import errors
from ...models.portfolio_error_response import PortfolioErrorResponse
from ...models.value_response import ValueResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/portfolio/{chainId}/{accounts}/value".format(
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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> ValueResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = ValueResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = PortfolioErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[ValueResponse]:
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
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ValueResponse]:
    """Get accounts' value

     Returns value of portfolio for a list of accounts.

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
        block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
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
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ValueResponse:
    """Get accounts' value

     Returns value of portfolio for a list of accounts.

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
        block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueResponse]
    """

    return sync_detailed(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
        block_number=block_number,
        timestamp=timestamp,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    accounts: List[str],
    *,
    tokens: Union[Unset, None, List[str]] = UNSET,
    quote_address: Union[Unset, None, str] = UNSET,
    include_positions: Union[Unset, None, bool] = UNSET,
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> Response[ValueResponse]:
    """Get accounts' value

     Returns value of portfolio for a list of accounts.

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
        block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        accounts=accounts,
        client=client,
        tokens=tokens,
        quote_address=quote_address,
        include_positions=include_positions,
        block_number=block_number,
        timestamp=timestamp,
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
    block_number: Union[Unset, None, float] = UNSET,
    timestamp: Union[Unset, None, float] = UNSET,
    client: "Credmark",
) -> ValueResponse:
    """Get accounts' value

     Returns value of portfolio for a list of accounts.

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
        block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
            latest block.
        timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
            instead of a block number. Finds a block at or before the number of seconds since January
            1, 1970.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ValueResponse]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            accounts=accounts,
            client=client,
            tokens=tokens,
            quote_address=quote_address,
            include_positions=include_positions,
            block_number=block_number,
            timestamp=timestamp,
        )
    ).parsed
