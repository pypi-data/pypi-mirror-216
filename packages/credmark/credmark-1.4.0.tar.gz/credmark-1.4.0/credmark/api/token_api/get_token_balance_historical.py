from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict, Union

import httpx

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Union

from ... import errors
from ...models.token_balance_historical_response import TokenBalanceHistoricalResponse
from ...models.token_error_response import TokenErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chain_id: int,
    token_address: str,
    *,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    client: "Credmark",
) -> Dict[str, Any]:
    url = "{}/v1/tokens/{chainId}/{tokenAddress}/balance/historical".format(
        client.base_url, chainId=chain_id, tokenAddress=token_address
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["startBlockNumber"] = start_block_number

    params["endBlockNumber"] = end_block_number

    params["blockInterval"] = block_interval

    params["startTimestamp"] = start_timestamp

    params["endTimestamp"] = end_timestamp

    params["timeInterval"] = time_interval

    params["accountAddress"] = account_address

    params["quoteAddress"] = quote_address

    params["scaled"] = scaled

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


def _parse_response(*, client: "Credmark", response: httpx.Response) -> TokenBalanceHistoricalResponse:
    if response.status_code == HTTPStatus.OK:
        response_200 = TokenBalanceHistoricalResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = TokenErrorResponse.from_dict(response.json())

        raise errors.CredmarkError(response.status_code, response.content, response_400)
    raise errors.CredmarkError(response.status_code, response.content)


def _build_response(*, client: "Credmark", response: httpx.Response) -> Response[TokenBalanceHistoricalResponse]:
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
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    client: "Credmark",
) -> Response[TokenBalanceHistoricalResponse]:
    """Get historical balance

     Returns historical token balance for an account.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        start_block_number (Union[Unset, None, float]): Start block number of the balance.
            Defaults to token's creation block.
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
        account_address (str): The address of the account for which balance of the token will be
            fetched.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
            Default: True.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenBalanceHistoricalResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
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
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    client: "Credmark",
) -> TokenBalanceHistoricalResponse:
    """Get historical balance

     Returns historical token balance for an account.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        start_block_number (Union[Unset, None, float]): Start block number of the balance.
            Defaults to token's creation block.
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
        account_address (str): The address of the account for which balance of the token will be
            fetched.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
            Default: True.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenBalanceHistoricalResponse]
    """

    return sync_detailed(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
    ).parsed


async def asyncio_detailed(
    chain_id: int,
    token_address: str,
    *,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    client: "Credmark",
) -> Response[TokenBalanceHistoricalResponse]:
    """Get historical balance

     Returns historical token balance for an account.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        start_block_number (Union[Unset, None, float]): Start block number of the balance.
            Defaults to token's creation block.
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
        account_address (str): The address of the account for which balance of the token will be
            fetched.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
            Default: True.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenBalanceHistoricalResponse]
    """

    kwargs = _get_kwargs(
        chain_id=chain_id,
        token_address=token_address,
        client=client,
        start_block_number=start_block_number,
        end_block_number=end_block_number,
        block_interval=block_interval,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        time_interval=time_interval,
        account_address=account_address,
        quote_address=quote_address,
        scaled=scaled,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    chain_id: int,
    token_address: str,
    *,
    start_block_number: Union[Unset, None, float] = UNSET,
    end_block_number: Union[Unset, None, float] = UNSET,
    block_interval: Union[Unset, None, float] = UNSET,
    start_timestamp: Union[Unset, None, float] = UNSET,
    end_timestamp: Union[Unset, None, float] = UNSET,
    time_interval: Union[Unset, None, float] = UNSET,
    account_address: str,
    quote_address: Union[Unset, None, str] = UNSET,
    scaled: Union[Unset, None, bool] = True,
    client: "Credmark",
) -> TokenBalanceHistoricalResponse:
    """Get historical balance

     Returns historical token balance for an account.

    Args:
        chain_id (int): Chain identifier. This endpoint supports the following chains

            `1` - Mainnet
        token_address (str): The address of the token requested.
        start_block_number (Union[Unset, None, float]): Start block number of the balance.
            Defaults to token's creation block.
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
        account_address (str): The address of the account for which balance of the token will be
            fetched.
        quote_address (Union[Unset, None, str]): The address of the token/currency used as the
            currency of the returned price. Defaults to USD (address
            `0x0000000000000000000000000000000000000348`).
        scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
            Default: True.

    Raises:
        errors.CredmarkError: If the server returns a non 2xx status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TokenBalanceHistoricalResponse]
    """

    return (
        await asyncio_detailed(
            chain_id=chain_id,
            token_address=token_address,
            client=client,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
        )
    ).parsed
