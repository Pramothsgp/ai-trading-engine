import httpx
import asyncio
from typing import Dict, Any, Optional
from backend.schemas.strategy import StrategyConfig


class AsyncTradingClient:
    """Async client for trading system API calls"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000/api", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def get_signals(
        self, strategy: StrategyConfig, date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get signals for a specific strategy.

        Args:
            strategy: Strategy configuration
            date: Optional date in YYYY-MM-DD format. If not provided, uses latest data (live)

        Returns:
            Dictionary containing signals and date information
        """
        params = {}
        if date:
            params["date"] = date

        try:
            response = await self.client.post(
                "/signals/date", json=strategy.dict(), params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to get signals: {e}")

    async def get_live_signals(
        self, strategy: StrategyConfig, top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Get live signals for a specific strategy.

        Args:
            strategy: Strategy configuration
            top_k: Number of top signals to return

        Returns:
            Dictionary containing live signals
        """
        try:
            response = await self.client.post(
                "/signals/live", json=strategy.dict(), params={"top_k": top_k}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to get live signals: {e}")

    async def get_backtest(self, strategy: StrategyConfig) -> Dict[str, Any]:
        """
        Get backtest results for a strategy.

        Args:
            strategy: Strategy configuration

        Returns:
            Dictionary containing backtest results
        """
        try:
            response = await self.client.post("/backtest/run", json=strategy.dict())
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Failed to get backtest: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Dictionary containing health status
        """
        try:
            response = await self.client.get("/")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"Health check failed: {e}")


# Convenience function for quick usage
async def get_aclient(
    base_url: str = "http://127.0.0.1:8000/api", timeout: int = 30
) -> AsyncTradingClient:
    """Create an async trading client instance"""
    return AsyncTradingClient(base_url, timeout)


# Example usage:
# async def main():
#     async with get_aclient() as client:
#         strategy = StrategyConfig(
#             alphas={"ml": AlphaConfig(enabled=True, weight=0.5)},
#             top_k=5
#         )
#
#         # Get signals without date (uses live data)
#         signals = await client.get_signals(strategy)
#         print(signals)
#
#         # Get signals for specific date
#         signals_with_date = await client.get_signals(strategy, date="2024-01-15")
#         print(signals_with_date)
#
# if __name__ == "__main__":
#     asyncio.run(main())
