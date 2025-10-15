# Blockchain Analytics Dashboard

**Author:** Fidel

## Purpose

This dashboard provides comprehensive visualization and analysis of on-chain blockchain data. It enables users to track and analyze:

- **Whale Movements**: Monitor large-scale cryptocurrency transactions and wallet activities
- **Mempool Statistics**: Real-time analysis of pending transactions and network congestion
- **DeFi Analytics**: Track decentralized finance protocols, liquidity pools, and yield farming opportunities

## Core Technologies

- **Python**: Primary programming language for data processing and backend logic
- **R**: Statistical analysis and advanced data modeling
- **Jupyter**: Interactive notebooks for exploratory data analysis
- **Plotly**: Interactive data visualizations and dashboards
- **Web3.py**: Ethereum blockchain interaction and smart contract integration
- **Etherscan API**: Historical blockchain data and transaction analysis

## Use Cases

- **Whale Watching**: Identify and track large holders' transaction patterns to anticipate market movements
- **Network Monitoring**: Analyze mempool congestion to optimize transaction timing and gas fees
- **DeFi Portfolio Tracking**: Monitor protocol TVL (Total Value Locked), APY rates, and impermanent loss
- **Market Intelligence**: Correlate on-chain metrics with price action for trading strategies
- **Risk Assessment**: Analyze smart contract interactions and wallet behaviors for security insights

## Sample Features

- Real-time whale transaction alerts with threshold customization
- Interactive mempool heatmaps showing gas price distribution
- DeFi protocol comparison dashboards with historical performance metrics
- Automated reports for daily/weekly on-chain activity summaries
- Custom wallet tracking with notification capabilities

## Project Structure

```
blockchain-analytics-dashboard/
│
├── README.md
│
├── notebooks/
│   ├── exploratory_analysis.ipynb       # Initial data exploration
│   ├── whale_tracking_analysis.ipynb    # Whale movement analysis
│   ├── mempool_statistics.ipynb         # Mempool data analysis
│   └── defi_analytics.ipynb             # DeFi protocol analysis
│
├── scripts/
│   ├── data_collection/
│   │   ├── web3_connector.py            # Web3.py blockchain connections
│   │   ├── etherscan_fetcher.py         # Etherscan API data retrieval
│   │   └── mempool_monitor.py           # Real-time mempool monitoring
│   │
│   ├── data_processing/
│   │   ├── transaction_parser.py        # Parse and clean transaction data
│   │   ├── whale_detector.py            # Identify whale transactions
│   │   └── defi_aggregator.py           # Aggregate DeFi protocol data
│   │
│   ├── visualization/
│   │   ├── plotly_dashboards.py         # Interactive Plotly dashboards
│   │   ├── whale_charts.py              # Whale activity visualizations
│   │   └── mempool_heatmaps.py          # Mempool statistics charts
│   │
│   └── r_scripts/
│       ├── statistical_models.R         # R-based statistical analysis
│       └── time_series_analysis.R       # Time series forecasting
│
├── data/
│   ├── raw/                             # Raw blockchain data
│   ├── processed/                       # Cleaned and processed datasets
│   └── cache/                           # Cached API responses
│
├── config/
│   ├── api_keys.example.json            # Example API configuration
│   └── dashboard_settings.json          # Dashboard configuration
│
├── requirements.txt                      # Python dependencies
└── environment.yml                       # Conda environment specification
```

## Getting Started

1. Clone the repository
2. Install dependencies from `requirements.txt`
3. Configure API keys in `config/`
4. Run Jupyter notebooks in `notebooks/` for exploratory analysis
5. Execute scripts in `scripts/` for automated data collection and processing

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available for educational and research purposes.
