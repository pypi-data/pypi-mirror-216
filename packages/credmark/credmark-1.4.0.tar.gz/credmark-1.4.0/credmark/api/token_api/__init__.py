from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Credmark

from typing import Dict, Optional, Union, cast

from ...models.get_token_price_historical_src import GetTokenPriceHistoricalSrc
from ...models.get_token_price_src import GetTokenPriceSrc
from ...models.token_abi_response import TokenAbiResponse
from ...models.token_balance_historical_response import TokenBalanceHistoricalResponse
from ...models.token_balance_response import TokenBalanceResponse
from ...models.token_creation_block_response import TokenCreationBlockResponse
from ...models.token_decimals_response import TokenDecimalsResponse
from ...models.token_error_response import TokenErrorResponse
from ...models.token_historical_holders_count_response import TokenHistoricalHoldersCountResponse
from ...models.token_holders_count_response import TokenHoldersCountResponse
from ...models.token_holders_response import TokenHoldersResponse
from ...models.token_logo_response import TokenLogoResponse
from ...models.token_metadata_response import TokenMetadataResponse
from ...models.token_name_response import TokenNameResponse
from ...models.token_price_historical_response import TokenPriceHistoricalResponse
from ...models.token_price_response import TokenPriceResponse
from ...models.token_symbol_response import TokenSymbolResponse
from ...models.token_total_supply_historical_response import TokenTotalSupplyHistoricalResponse
from ...models.token_total_supply_response import TokenTotalSupplyResponse
from ...models.token_volume_historical_response import TokenVolumeHistoricalResponse
from ...models.token_volume_response import TokenVolumeResponse
from ...types import UNSET, Unset
from . import (
    get_token_abi,
    get_token_balance,
    get_token_balance_historical,
    get_token_creation_block,
    get_token_decimals,
    get_token_holders,
    get_token_holders_count,
    get_token_holders_count_historical,
    get_token_logo,
    get_token_metadata,
    get_token_name,
    get_token_price,
    get_token_price_historical,
    get_token_symbol,
    get_token_total_supply,
    get_token_total_supply_historical,
    get_token_volume,
    get_token_volume_historical,
)


class TokenApi:
    def __init__(self, client: "Credmark"):
        self.__client = client

    def get_token_metadata(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
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

        return get_token_metadata.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_metadata_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
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

        return await get_token_metadata.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_name(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenNameResponse:
        """Get token name

         Returns name of a token.

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
            block_number (Union[Unset, None, float]): Block number of the name. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenNameResponse]
        """

        return get_token_name.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_name_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenNameResponse:
        """Get token name

         Returns name of a token.

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
            block_number (Union[Unset, None, float]): Block number of the name. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenNameResponse]
        """

        return await get_token_name.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_symbol(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenSymbolResponse:
        """Get token symbol

         Returns symbol of a token.

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
            block_number (Union[Unset, None, float]): Block number of the symbol. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenSymbolResponse]
        """

        return get_token_symbol.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_symbol_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenSymbolResponse:
        """Get token symbol

         Returns symbol of a token.

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
            block_number (Union[Unset, None, float]): Block number of the symbol. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenSymbolResponse]
        """

        return await get_token_symbol.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_decimals(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenDecimalsResponse:
        """Get token decimals

         Returns decimals of a token.

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
            block_number (Union[Unset, None, float]): Block number of the decimals. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenDecimalsResponse]
        """

        return get_token_decimals.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_decimals_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenDecimalsResponse:
        """Get token decimals

         Returns decimals of a token.

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
            block_number (Union[Unset, None, float]): Block number of the decimals. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenDecimalsResponse]
        """

        return await get_token_decimals.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_total_supply(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> TokenTotalSupplyResponse:
        """Get token's total supply

         Returns total supply of a token.

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
            block_number (Union[Unset, None, float]): Block number of the total supply. Defaults to
                the latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.
            scaled (Union[Unset, None, bool]): Scale total supply by token decimals. Defaults to
                `true`. Default: True.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenTotalSupplyResponse]
        """

        return get_token_total_supply.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
            scaled=scaled,
        )

    async def get_token_total_supply_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> TokenTotalSupplyResponse:
        """Get token's total supply

         Returns total supply of a token.

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
            block_number (Union[Unset, None, float]): Block number of the total supply. Defaults to
                the latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.
            scaled (Union[Unset, None, bool]): Scale total supply by token decimals. Defaults to
                `true`. Default: True.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenTotalSupplyResponse]
        """

        return await get_token_total_supply.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
            scaled=scaled,
        )

    def get_token_total_supply_historical(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> TokenTotalSupplyHistoricalResponse:
        """Get historical total supply

         Returns historical total supply for a token.

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
            scaled (Union[Unset, None, bool]): Scale total supply by token decimals. Defaults to
                `true`. Default: True.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenTotalSupplyHistoricalResponse]
        """

        return get_token_total_supply_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            scaled=scaled,
        )

    async def get_token_total_supply_historical_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        scaled: Union[Unset, None, bool] = True,
    ) -> TokenTotalSupplyHistoricalResponse:
        """Get historical total supply

         Returns historical total supply for a token.

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
            scaled (Union[Unset, None, bool]): Scale total supply by token decimals. Defaults to
                `true`. Default: True.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenTotalSupplyHistoricalResponse]
        """

        return await get_token_total_supply_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            scaled=scaled,
        )

    def get_token_logo(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenLogoResponse:
        """Get token logo

         Returns logo of a token.

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
            block_number (Union[Unset, None, float]): Block number of the logo. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenLogoResponse]
        """

        return get_token_logo.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_logo_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenLogoResponse:
        """Get token logo

         Returns logo of a token.

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
            block_number (Union[Unset, None, float]): Block number of the logo. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenLogoResponse]
        """

        return await get_token_logo.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_creation_block(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenCreationBlockResponse:
        """Get token creation block

         Returns creation block number of a token.

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
            block_number (Union[Unset, None, float]): Block number of the token. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenCreationBlockResponse]
        """

        return get_token_creation_block.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_creation_block_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenCreationBlockResponse:
        """Get token creation block

         Returns creation block number of a token.

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
            block_number (Union[Unset, None, float]): Block number of the token. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenCreationBlockResponse]
        """

        return await get_token_creation_block.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_abi(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenAbiResponse:
        """Get token ABI

         Returns ABI of a token.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            block_number (Union[Unset, None, float]): Block number of the ABI. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenAbiResponse]
        """

        return get_token_abi.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_abi_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenAbiResponse:
        """Get token ABI

         Returns ABI of a token.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            block_number (Union[Unset, None, float]): Block number of the ABI. Defaults to the latest
                block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenAbiResponse]
        """

        return await get_token_abi.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_price(
        self,
        chain_id: int,
        token_address: str,
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    ) -> TokenPriceResponse:
        """Get token price data

         Returns price data for a token.

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
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            block_number (Union[Unset, None, float]): Block number of the price quote. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.
            src (Union[Unset, None, GetTokenPriceSrc]): (Optional) specify preferred source to be
                queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to
                price.quote model) Default: GetTokenPriceSrc.DEX.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenPriceResponse]
        """

        return get_token_price.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
            src=src,
        )

    async def get_token_price_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        quote_address: Union[Unset, None, str] = UNSET,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
        src: Union[Unset, None, GetTokenPriceSrc] = GetTokenPriceSrc.DEX,
    ) -> TokenPriceResponse:
        """Get token price data

         Returns price data for a token.

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
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            block_number (Union[Unset, None, float]): Block number of the price quote. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.
            src (Union[Unset, None, GetTokenPriceSrc]): (Optional) specify preferred source to be
                queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to
                price.quote model) Default: GetTokenPriceSrc.DEX.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenPriceResponse]
        """

        return await get_token_price.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            quote_address=quote_address,
            block_number=block_number,
            timestamp=timestamp,
            src=src,
        )

    def get_token_price_historical(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        src: Union[Unset, None, GetTokenPriceHistoricalSrc] = GetTokenPriceHistoricalSrc.DEX,
    ) -> TokenPriceHistoricalResponse:
        """Get historical price

         Returns historical price data for a token.

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
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            src (Union[Unset, None, GetTokenPriceHistoricalSrc]): (Optional) specify preferred source
                to be queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to
                price.quote model) Default: GetTokenPriceHistoricalSrc.DEX.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenPriceHistoricalResponse]
        """

        return get_token_price_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            quote_address=quote_address,
            src=src,
        )

    async def get_token_price_historical_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        src: Union[Unset, None, GetTokenPriceHistoricalSrc] = GetTokenPriceHistoricalSrc.DEX,
    ) -> TokenPriceHistoricalResponse:
        """Get historical price

         Returns historical price data for a token.

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
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            src (Union[Unset, None, GetTokenPriceHistoricalSrc]): (Optional) specify preferred source
                to be queried first, choices: "dex" (pre-calculated, default), or "cex" (from call to
                price.quote model) Default: GetTokenPriceHistoricalSrc.DEX.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenPriceHistoricalResponse]
        """

        return await get_token_price_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
            quote_address=quote_address,
            src=src,
        )

    def get_token_balance(
        self,
        chain_id: int,
        token_address: str,
        *,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenBalanceResponse:
        """Get token balance

         Returns token balance for an account.

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
            account_address (str): The address of the account for which balance of the token will be
                fetched.
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
                Default: True.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenBalanceResponse]
        """

        return get_token_balance.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_balance_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        account_address: str,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenBalanceResponse:
        """Get token balance

         Returns token balance for an account.

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
            account_address (str): The address of the account for which balance of the token will be
                fetched.
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            scaled (Union[Unset, None, bool]): Scale balance by token decimals. Defaults to `true`.
                Default: True.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenBalanceResponse]
        """

        return await get_token_balance.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            account_address=account_address,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_balance_historical(
        self,
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

        return get_token_balance_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
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

    async def get_token_balance_historical_async(
        self,
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

        return await get_token_balance_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
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

    def get_token_volume(
        self,
        chain_id: int,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
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

        return get_token_volume.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    async def get_token_volume_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
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

        return await get_token_volume.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )

    def get_token_volume_historical(
        self,
        chain_id: int,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> TokenVolumeHistoricalResponse:
        """Get historical volume

         Returns traded volume for a token over a period of blocks or time divided by intervals.

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
            block_interval (Union[Unset, None, float]): Number of blocks between each data point.
            time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
                Should be in seconds. Defaults to 86,400.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenVolumeHistoricalResponse]
        """

        return get_token_volume_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            block_interval=block_interval,
            time_interval=time_interval,
        )

    async def get_token_volume_historical_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        scaled: Union[Unset, None, bool] = True,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> TokenVolumeHistoricalResponse:
        """Get historical volume

         Returns traded volume for a token over a period of blocks or time divided by intervals.

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
            block_interval (Union[Unset, None, float]): Number of blocks between each data point.
            time_interval (Union[Unset, None, float]): Can be specified instead of blockInterval.
                Should be in seconds. Defaults to 86,400.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenVolumeHistoricalResponse]
        """

        return await get_token_volume_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            scaled=scaled,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            block_interval=block_interval,
            time_interval=time_interval,
        )

    def get_token_holders(
        self,
        chain_id: int,
        token_address: str,
        *,
        page_size: float = 100.0,
        cursor: Union[Unset, None, str] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenHoldersResponse:
        """Get token holders

         Returns holders of a token at a block or time.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            page_size (float): The size of the returned page. Do not change this from page to page
                when using a cursor. Default: 100.0.
            cursor (Union[Unset, None, str]): The cursor from the results of a previous page. Use
                empty string (or undefined/null) for first page.
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            scaled (Union[Unset, None, bool]): Scale holders' balance by token decimals. Defaults to
                `true`. Default: True.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block. Do not change this from page to page when using a cursor.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHoldersResponse]
        """

        return get_token_holders.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            page_size=page_size,
            cursor=cursor,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_holders_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        page_size: float = 100.0,
        cursor: Union[Unset, None, str] = UNSET,
        quote_address: Union[Unset, None, str] = UNSET,
        scaled: Union[Unset, None, bool] = True,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenHoldersResponse:
        """Get token holders

         Returns holders of a token at a block or time.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            page_size (float): The size of the returned page. Do not change this from page to page
                when using a cursor. Default: 100.0.
            cursor (Union[Unset, None, str]): The cursor from the results of a previous page. Use
                empty string (or undefined/null) for first page.
            quote_address (Union[Unset, None, str]): The address of the token/currency used as the
                currency of the returned price. Defaults to USD (address
                `0x0000000000000000000000000000000000000348`).
            scaled (Union[Unset, None, bool]): Scale holders' balance by token decimals. Defaults to
                `true`. Default: True.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block. Do not change this from page to page when using a cursor.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHoldersResponse]
        """

        return await get_token_holders.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            page_size=page_size,
            cursor=cursor,
            quote_address=quote_address,
            scaled=scaled,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_holders_count(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenHoldersCountResponse:
        """Get total number of token holders

         Returns total number of holders of a token at a block or time.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block. Do not change this from page to page when using a cursor.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHoldersCountResponse]
        """

        return get_token_holders_count.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    async def get_token_holders_count_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        block_number: Union[Unset, None, float] = UNSET,
        timestamp: Union[Unset, None, float] = UNSET,
    ) -> TokenHoldersCountResponse:
        """Get total number of token holders

         Returns total number of holders of a token at a block or time.

        Args:
            chain_id (int): Chain identifier. This endpoint supports the following chains

                `1` - Mainnet
            token_address (str): The address of the token requested.
            block_number (Union[Unset, None, float]): Block number of the balance. Defaults to the
                latest block. Do not change this from page to page when using a cursor.
            timestamp (Union[Unset, None, float]): Timestamp of a block number can be specified
                instead of a block number. Finds a block at or before the number of seconds since January
                1, 1970.

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHoldersCountResponse]
        """

        return await get_token_holders_count.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            block_number=block_number,
            timestamp=timestamp,
        )

    def get_token_holders_count_historical(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> TokenHistoricalHoldersCountResponse:
        """Get historical total number of token holders

         Returns historical total number of holders of a token at a block or time.

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

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHistoricalHoldersCountResponse]
        """

        return get_token_holders_count_historical.sync(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )

    async def get_token_holders_count_historical_async(
        self,
        chain_id: int,
        token_address: str,
        *,
        start_block_number: Union[Unset, None, float] = UNSET,
        end_block_number: Union[Unset, None, float] = UNSET,
        block_interval: Union[Unset, None, float] = UNSET,
        start_timestamp: Union[Unset, None, float] = UNSET,
        end_timestamp: Union[Unset, None, float] = UNSET,
        time_interval: Union[Unset, None, float] = UNSET,
    ) -> TokenHistoricalHoldersCountResponse:
        """Get historical total number of token holders

         Returns historical total number of holders of a token at a block or time.

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

        Raises:
            errors.CredmarkError: If the server returns a non 2xx status code.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TokenHistoricalHoldersCountResponse]
        """

        return await get_token_holders_count_historical.asyncio(
            client=self.__client,
            chain_id=chain_id,
            token_address=token_address,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            block_interval=block_interval,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            time_interval=time_interval,
        )
