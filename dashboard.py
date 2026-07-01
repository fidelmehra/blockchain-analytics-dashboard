# Blockchain Analytics Dashboard - Author: Fidel Mehra
# Stack: Streamlit + Plotly + requests (CoinGecko public API)
# Run: streamlit run dashboard.py

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Blockchain Analytics", layout="wide", page_icon="")

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------
BASE = "https://api.coingecko.com/api/v3"

def get_price_history(coin_id="bitcoin", days=30, currency="usd"):
    url = f"{BASE}/coins/{coin_id}/market_chart"
    r = requests.get(url, params={"vs_currency": currency, "days": days}, timeout=10)
    data = r.json()
    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def get_top_coins(n=10):
    url = f"{BASE}/coins/markets"
    r = requests.get(url, params={"vs_currency": "usd", "order": "market_cap_desc",
                                   "per_page": n, "page": 1}, timeout=10)
    return pd.DataFrame(r.json())

def get_global_data():
    r = requests.get(f"{BASE}/global", timeout=10)
    return r.json().get("data", {})

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
st.sidebar.title("Blockchain Analytics")
st.sidebar.markdown("*Author: Fidel Mehra*")
coin_options = {"Bitcoin": "bitcoin", "Ethereum": "ethereum", "Solana": "solana",
                "BNB": "binancecoin", "XRP": "ripple"}
selected_coin_name = st.sidebar.selectbox("Select Coin", list(coin_options.keys()))
selected_coin = coin_options[selected_coin_name]
days = st.sidebar.slider("Price History (days)", 7, 365, 30)
top_n = st.sidebar.slider("Top N Coins by Market Cap", 5, 25, 10)

# -------------------------------------------------------
# Main Layout
# -------------------------------------------------------
st.title("Blockchain Analytics Dashboard")
st.markdown("Real-time on-chain data powered by CoinGecko public API.")

# Row 1: Global stats
st.subheader("Global Market Overview")
try:
    gdata = get_global_data()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Cryptocurrencies", f"{gdata.get('active_cryptocurrencies', 'N/A'):,}")
    col2.metric("Total Market Cap (USD)", f"${gdata.get('total_market_cap', {}).get('usd', 0)/1e12:.2f}T")
    col3.metric("24h Volume (USD)", f"${gdata.get('total_volume', {}).get('usd', 0)/1e9:.1f}B")
    col4.metric("BTC Dominance", f"{gdata.get('market_cap_percentage', {}).get('btc', 0):.1f}%")
except Exception as e:
    st.warning(f"Could not fetch global data: {e}")

st.divider()

# Row 2: Price chart
st.subheader(f"{selected_coin_name} Price History ({days} days)")
try:
    price_df = get_price_history(selected_coin, days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_df["date"], y=price_df["price"],
                             mode="lines", name=selected_coin_name,
                             line=dict(color="#F7931A", width=2)))
    fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)",
                      template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Could not fetch price data: {e}")

st.divider()

# Row 3: Top coins table + market cap bar
st.subheader(f"Top {top_n} Coins by Market Cap")
try:
    coins_df = get_top_coins(top_n)
    cols_to_show = ["name", "symbol", "current_price", "market_cap",
                    "price_change_percentage_24h", "total_volume"]
    coins_df = coins_df[[c for c in cols_to_show if c in coins_df.columns]]
    coins_df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Change %", "Volume"]
    st.dataframe(coins_df.style.format({
        "Price (USD)": "${:,.2f}", "Market Cap": "${:,.0f}",
        "24h Change %": "{:.2f}%", "Volume": "${:,.0f}"
    }), use_container_width=True)

    fig2 = px.bar(coins_df, x="Name", y="Market Cap", color="24h Change %",
                  color_continuous_scale="RdYlGn", template="plotly_dark",
                  title="Market Cap Distribution")
    st.plotly_chart(fig2, use_container_width=True)
except Exception as e:
    st.error(f"Could not fetch market data: {e}")

st.caption(f"Data from CoinGecko | Last refreshed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
