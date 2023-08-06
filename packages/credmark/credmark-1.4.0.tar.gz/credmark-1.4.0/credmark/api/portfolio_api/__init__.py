from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, List, Optional, Union, cast

from ...models.portfolio_error_response import PortfolioErrorResponse
from ...models.positions_historical_response import PositionsHistoricalResponse
from ...models.positions_response import PositionsResponse
from ...models.returns_response import ReturnsResponse
from ...models.value_historical_response import ValueHistoricalResponse
from ...models.value_response import ValueResponse
from ...types import UNSET, Unset
from . import get_positions, get_positions_historical, get_returns, get_value, get_value_historical


class PortfolioApi:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def get_positions(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        tokens: Union[Unset, None, List[str]] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> PositionsResponse:
        """Get accounts' positions

         Returns positions for a list of accounts.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
            tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
                tokens are provided return positions for all tokens with non-zero balances.
            block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PositionsResponse]
        """

        return get_positions.sync(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            tokens=tokens,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_positions_async(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        tokens: Union[Unset, None, List[str]] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> PositionsResponse:
        """Get accounts' positions

         Returns positions for a list of accounts.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
            tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
                tokens are provided return positions for all tokens with non-zero balances.
            block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PositionsResponse]
        """

        return await get_positions.asyncio(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            tokens=tokens,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_positions_historical(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        tokens: Union[Unset, None, List[str]] = UNSET,
    ) -> PositionsHistoricalResponse:
        """Get accounts' historical positions

         Returns positions for a list of accounts over a series of blocks.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
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
            tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
                tokens are provided return positions for all tokens with non-zero balances.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PositionsHistoricalResponse]
        """

        return get_positions_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            tokens=tokens,
        )

    async def get_positions_historical_async(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        tokens: Union[Unset, None, List[str]] = UNSET,
    ) -> PositionsHistoricalResponse:
        """Get accounts' historical positions

         Returns positions for a list of accounts over a series of blocks.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
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
            tokens (Union[Unset, None, List[str]]): Comma separated list of token addresses. If no
                tokens are provided return positions for all tokens with non-zero balances.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PositionsHistoricalResponse]
        """

        return await get_positions_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            tokens=tokens,
        )

    def get_value(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        tokens: Union[Unset, None, List[str]] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        include_positions: Union[Unset, None, bool] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
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

        return get_value.sync(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            tokens=tokens,
            quote_address=quote_address,
            include_positions=include_positions,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_value_async(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        tokens: Union[Unset, None, List[str]] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        include_positions: Union[Unset, None, bool] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
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

        return await get_value.asyncio(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            tokens=tokens,
            quote_address=quote_address,
            include_positions=include_positions,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_value_historical(
        self,
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

        return get_value_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
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

    async def get_value_historical_async(
        self,
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

        return await get_value_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
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

    def get_returns(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> ReturnsResponse:
        """Get accounts' token returns

         Returns PnL of portfolio for a list of accounts.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency for price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ReturnsResponse]
        """

        return get_returns.sync(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_returns_async(
        self,
        chain_id: int,
        accounts: List[str],
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> ReturnsResponse:
        """Get accounts' token returns

         Returns PnL of portfolio for a list of accounts.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            accounts (List[str]): Comma separated list of account addresses
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency for price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            block_number (Union[Unset, None, float]): Block number of the portfolio. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ReturnsResponse]
        """

        return await get_returns.asyncio(
            client=self.__client,
            chain_id=chain_id,
            accounts=accounts,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
        )
