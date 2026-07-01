"""
fetcher.py  -  On-chain data fetcher for Blockchain Analytics Dashboard

Provides:
  - fetch_eth_price()         : latest ETH/USD price via CoinGecko
  - fetch_gas_stats()         : current gas prices via Etherscan
  - fetch_whale_txns()        : recent large ETH transfers (>= threshold)
  - fetch_defi_tvl(protocol)  : DeFi TVL from DeFi Llama
  - fetch_mempool_stats()     : pending tx count from Etherscan

All functions return plain dicts / lists so the dashboard can render them
without touching raw HTTP.
"""

import os
import time
import requests
from typing import Any

# ---------------------------------------------------------------------------
# Config  (override via env vars)
# ---------------------------------------------------------------------------
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY", "YourApiKeyToken")
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
ETHERSCAN_BASE = "https://api.etherscan.io/api"
DEFI_LLAMA_BASE = "https://api.llama.fi"

WHALE_THRESHOLD_ETH = 100  # flag transfers >= 100 ETH

SESSION = requests.Session()
SESSION.headers.update({"Accept": "application/json", "User-Agent": "blockchain-analytics-dashboard/1.0"})


def _get(url: str, params: dict | None = None, timeout: int = 10) -> Any:
    """Thin wrapper around requests.get with basic retry."""
    for attempt in range(3):
        try:
            r = SESSION.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as exc:
            if attempt == 2:
                raise
            time.sleep(1.5 ** attempt)


# ---------------------------------------------------------------------------
# Price
# ---------------------------------------------------------------------------
def fetch_eth_price() -> dict:
    """
    Returns {'usd': float, 'usd_24h_change': float, 'usd_market_cap': float}
    """
    data = _get(
        f"{COINGECKO_BASE}/simple/price",
        params={"ids": "ethereum", "vs_currencies": "usd",
                "include_24hr_change": "true", "include_market_cap": "true"}
    )
    eth = data.get("ethereum", {})
    return {
        "usd":             eth.get("usd", 0),
        "usd_24h_change":  eth.get("usd_24h_change", 0),
        "usd_market_cap": eth.get("usd_market_cap", 0),
    }


# ---------------------------------------------------------------------------
# Gas
# ---------------------------------------------------------------------------
def fetch_gas_stats() -> dict:
    """
    Returns {'safe': int, 'propose': int, 'fast': int}  (Gwei)
    """
    data = _get(
        ETHERSCAN_BASE,
        params={"module": "gastracker", "action": "gasoracle", "apikey": ETHERSCAN_KEY}
    )
    result = data.get("result", {})
    return {
        "safe":    int(result.get("SafeGasPrice",    0)),
        "propose": int(result.get("ProposeGasPrice", 0)),
        "fast":    int(result.get("FastGasPrice",    0)),
    }


# ---------------------------------------------------------------------------
# Whale transactions
# ---------------------------------------------------------------------------
def fetch_whale_txns(pages: int = 1) -> list[dict]:
    """
    Returns recent ETH transfers >= WHALE_THRESHOLD_ETH.
    Each item: {'hash', 'from', 'to', 'value_eth', 'timestamp'}
    """
    whales = []
    for page in range(1, pages + 1):
        data = _get(
            ETHERSCAN_BASE,
            params={
                "module": "account",
                "action": "txlist",
                "address": "0x00000000219ab540356cBB839Cbe05303d7705Fa",  # ETH2 deposit contract
                "startblock": 0,
                "endblock": 99999999,
                "page": page,
                "offset": 50,
                "sort": "desc",
                "apikey": ETHERSCAN_KEY,
            }
        )
        txns = data.get("result", [])
        if not isinstance(txns, list):
            break
        for tx in txns:
            try:
                value_eth = int(tx["value"]) / 1e18
            except (KeyError, ValueError):
                continue
            if value_eth >= WHALE_THRESHOLD_ETH:
                whales.append({
                    "hash":       tx.get("hash", ""),
                    "from":       tx.get("from", ""),
                    "to":         tx.get("to", ""),
                    "value_eth":  round(value_eth, 4),
                    "timestamp":  int(tx.get("timeStamp", 0)),
                })
    return whales


# ---------------------------------------------------------------------------
# DeFi TVL
# ---------------------------------------------------------------------------
def fetch_defi_tvl(protocol: str = "uniswap") -> dict:
    """
    Returns {'name': str, 'tvl': float, 'chain': str, 'change_1d': float}
    """
    data = _get(f"{DEFI_LLAMA_BASE}/protocol/{protocol}")
    tvl_data = data.get("currentChainTvls", {})
    chain = max(tvl_data, key=lambda k: tvl_data[k], default="unknown")
    return {
        "name":      data.get("name", protocol),
        "tvl":       data.get("tvl", 0),
        "chain":     chain,
        "change_1d": data.get("change_1d", 0),
    }


# ---------------------------------------------------------------------------
# Mempool
# ---------------------------------------------------------------------------
def fetch_mempool_stats() -> dict:
    """
    Returns {'pending': int, 'queued': int} tx counts.
    """
    data = _get(
        ETHERSCAN_BASE,
        params={"module": "proxy", "action": "eth_getBlockTransactionCountByNumber",
                "tag": "pending", "apikey": ETHERSCAN_KEY}
    )
    pending_hex = data.get("result", "0x0")
    return {
        "pending": int(pending_hex, 16) if isinstance(pending_hex, str) else 0,
        "queued":  0,  # not directly available via public Etherscan
    }


# ---------------------------------------------------------------------------
# CLI quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    print("ETH Price:",   json.dumps(fetch_eth_price(),  indent=2))
    print("Gas Stats:",   json.dumps(fetch_gas_stats(),  indent=2))
    print("Mempool:",     json.dumps(fetch_mempool_stats(), indent=2))
    print("Uniswap TVL:", json.dumps(fetch_defi_tvl("uniswap"), indent=2))
