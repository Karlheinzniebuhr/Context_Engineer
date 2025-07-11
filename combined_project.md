# IMPLEMENTATION GUIDE GENERATION SYSTEM

You are a guide generation specialist. Your role is to create step-by-step implementation guides that less capable AI programming agents can follow successfully to build working systems.

**CRITICAL UNDERSTANDING**: Your output will be given to a less capable AI agent that must implement the entire system by following your guide. The guide must be foolproof.

## GUIDE GENERATION REQUIREMENTS

### 1. ABSOLUTE CLARITY
- Use numbered steps: "Step 1:", "Step 2:", etc.
- Each step must explain WHAT to do and WHY
- Provide exact commands with no ambiguity
- Include expected outputs for verification

### 2. ERROR PREVENTION  
- List all prerequisites before starting
- Specify exact versions of dependencies
- Include validation checks after each major step
- Provide troubleshooting for common issues

### 3. COMPLETE IMPLEMENTATION
- Include ALL necessary files with full content
- Provide complete directory structure
- Specify exact file paths and names
- Include all import statements and dependencies

### 4. VERIFICATION LOOPS
- After each section, include: "VERIFY: You should now see..."
- Provide test commands to confirm functionality
- Include expected error messages and fixes
- Add final verification checklist

### 5. COPY-PASTE READY
- All code blocks must be complete and runnable
- No placeholders like "YOUR_API_KEY" - specify where to get it
- Include full configuration files
- Provide exact terminal commands

## GUIDE STRUCTURE (MANDATORY)

### Phase 1: System Overview
- What the system does (1-2 sentences)
- Key components and their purposes
- Final outcome expectations

### Phase 2: Environment Setup
- Prerequisites checklist
- Installation commands (exact versions)
- Directory creation commands
- Verification steps

### Phase 3: Core Implementation
- Step-by-step file creation
- Complete code for each file
- Integration steps
- Testing at each stage

### Phase 4: Configuration
- Configuration file setup
- Environment variables
- API key configuration
- Final integration

### Phase 5: Testing & Validation
- Test commands
- Expected outputs
- Common issues and fixes
- Success verification

### Phase 6: Deployment
- Deployment preparation
- Launch commands
- Monitoring setup
- Maintenance procedures

## COMMUNICATION STYLE FOR LESS CAPABLE AI

- Use simple, direct language
- Avoid complex explanations or theory
- Provide concrete examples for everything
- Include exact copy-paste commands
- Specify expected results after each action
- Never assume the AI will understand context

## CRITICAL SUCCESS FACTORS

1. **NO AMBIGUITY**: Every instruction must have only one possible interpretation
2. **COMPLETE EXAMPLES**: All code must be complete, no partial snippets
3. **EXPLICIT VERIFICATION**: Tell the AI exactly what success looks like
4. **ERROR RECOVERY**: Provide solutions for when things go wrong
5. **STEP-BY-STEP**: Break complex tasks into the smallest possible steps

**REMEMBER**: The AI agent following your guide may not understand context, make logical leaps, or fill in missing details. Be completely explicit about every single step, file, command, and expectation.

# PROVIDED FILES ANALYSIS
========================


Generated: 2025-07-07T21:43:13.367567
Total files processed: 3
Valid files: 3

## FILE MANIFEST
==================================================

### Documentation Files:
- README.md (439 lines, 23594 bytes)

### Source Code Files:
- run_fractalbot_btc.py (178 lines, 7365 bytes)
- fractalbot.py (1637 lines, 80593 bytes)

==================================================

## FILE 1: README.md
**Path:** Fractal_Bot\README.md
**Type:** Documentation (.md)
**Size:** 439 lines, 23594 bytes
**Modified:** 2025-07-06T16:51:33.438803
==================================================
# Fractal Trading System

## Overview

The Fractal Trading System is a modular, AI-powered algorithmic trading platform designed for cryptocurrency futures. It operates through two distinct, co-operating components:

1. **FractalBot**: A sophisticated signal generation engine. It analyzes market history using Dynamic Time Warping (DTW) to find recurring fractal patterns and generates predictive trade signals.
2. **FractalTrader**: An automated execution engine. It listens for signals from the FractalBot, loads an optimized trading strategy, and manages the entire trade lifecycle on the Binance exchange.

This modular architecture allows for independent scaling, robust fault tolerance, and clear separation of concerns between market analysis and trade execution.

## System Architecture

### Connection Management (UPDATED)
The system includes a sophisticated **ConnectionManager** component that handles all WebSocket communications with Binance.  
**New in July 2025:** a `market_type` argument lets each bot choose the correct stream:

* `market_type='spot'` → uses the spot `/ws` stream (`start_kline_socket`) – **default**  
* `market_type='futures'` → uses the futures `/fapi/ws` stream (`start_kline_futures_socket`)

This allows different components to subscribe to the price feed they actually need (e.g. *FractalBot* analyses spot data, while *FractalTrader* executes on futures).  

**Optional Candle Heartbeat** – Set `log_1m_candles: true` in a bot's config (e.g. `run_fractalbot_btc.py`) to make the bot print every closed 1-minute candle (O/H/L/C). This is handy for quickly confirming that the price feed is alive before any signal is generated.

The ConnectionManager still provides:

- **Automatic Reconnection**: Detects connection failures and automatically reconnects with exponential backoff
- **Health Monitoring**: Continuously monitors connection health and data flow integrity
- **Timeout Handling**: Manages both connection timeouts and message timeouts to ensure data freshness
- **Network Resilience**: Includes DNS resolution checks and network connectivity verification
- **Resource Cleanup**: Properly manages WebSocket threads and prevents resource leaks
- **Event Loop Management**: Handles asyncio event loop resets to prevent conflicts during reconnections

Both FractalBot and FractalTrader use the ConnectionManager for reliable market data streaming and account updates.

### Signal Generation (FractalBot)
- Analyzes historical price patterns using **configurable Dynamic Time Warping (DTW) methods**:
  - **Standard DTW**: High-performance Numba/CPU implementation with various normalization methods
  - **ShapeDTW**: Advanced shape-based DTW that compares local patterns and handles normalization internally
- Generates **daily predictions** based on configurable parameters (weekly and monthly analysis are currently disabled)
- Creates pair-specific JSON signal files (e.g., `daily_prediction_signal_btc.json`) that contain a trade direction and summarized projection data
- **Chart Generation**: Saves prediction charts to `charts/` directory with consistent filenames (`daily_prediction_chart.png`) that are overwritten on each run
- **Notification System**: Supports both Discord and Telegram notifications with chart images
- Can run as a continuous, time-based service or in a one-shot "debug" mode for immediate analysis
- Triggers analysis based on the exchange's kline timestamps received via websocket, ensuring perfect synchronization with market data
- **Cross-Platform Compatibility**: Uses UTF-8 encoding for log files to support Unicode characters and emojis on all operating systems

### Trade Execution (FractalTrader)
- Uses an event-driven model, actively watching the file system for new signal files
- Upon signal detection, it loads a pre-optimized trading strategy from a JSON configuration file
- Executes trades by placing entry, take-profit, and stop-loss orders
- Supports both **live trading** on Binance and a full-featured **paper trading** mode for strategy validation without financial risk
- Logs are written to a log file named `fractal_trader_<symbol>.log` in each bot's directory (e.g., `bots/btc/fractal_trader_btc.log`) for easier debugging and organization
- Handles Ctrl+C (SIGINT) for a graceful shutdown, stopping all background threads and the file-watcher cleanly
- Calculates order quantities from real `availableBalance` (with leverage), splits across entries, applies `risk_per_trade`, and rounds down to exchange step sizes to prevent insufficient margin errors

## Project Structure

```
Fractal_Bot/
├── src/                              # Core Python modules
│   ├── fractalbot.py                 # FractalBot class (signal generation logic)
│   ├── fractalbot_standalone.py     # Standalone all-in-one implementation
│   ├── fractal_trader.py             # FractalTrader class (trade execution logic)
│   ├── DTW.py                        # Custom Dynamic Time Warping implementation
│   ├── shapeDTW.py                   # Shape-based Dynamic Time Warping implementation
│   ├── connection_manager.py         # Robust WebSocket connection management
│   ├── notification_manager.py       # Notification orchestration
│   ├── telegram_client.py            # Telegram bot integration
│   ├── discord_client.py             # Discord bot integration
│   └── __init__.py                   # Python package initializer
├── bots/                             # Individual bot instantiation scripts
│   ├── btc/
│   │   ├── run_fractalbot_btc.py    # RUN THIS: Starts the BTC signal generator
│   │   ├── run_trader_btc.py        # RUN THIS: Starts the BTC trader
│   │   ├── strategy_config_btc.json # UNIFIED: Complete strategy configuration
│   │   └── fractalbot_btc.log       # Log file for BTC signal generator
│   └── eth/
│       ├── run_fractalbot_eth.py    # RUN THIS: Starts the ETH signal generator
│       ├── run_trader_eth.py        # RUN THIS: Starts the ETH trader
│       ├── strategy_config_eth.json # UNIFIED: Complete strategy configuration
│       └── fractalbot_eth.log       # Log file for ETH signal generator
├── charts/                           # Generated prediction charts (auto-created)
│   └── daily_prediction_chart.png   # Latest daily prediction chart
├── data/                             # Historical data files (e.g., CSVs)
├── .env                              # Environment variables for API keys and credentials
├── .env.example                      # Template for environment variables
└── README.md                         # This file
```

## Legacy Standalone Implementation

The project includes a standalone version of the FractalBot (`src/fractalbot_standalone.py`) which was the original implementation before the system was refactored into its current modular architecture. This standalone version offers:

### Key Features
- **All-in-One Design**: Contains both signal generation and notification logic in a single file
- **Discord Integration**: Built-in Discord bot for sending trade signals and charts
- **Advanced DTW Analysis**: Implements various normalization methods and window-based pattern matching
- **Multi-Timeframe Analysis**: Supports daily, weekly, and monthly predictions
- **Robust Connection Management**: Integrated ConnectionManager for reliable WebSocket connections with automatic reconnection and health monitoring
- **Graceful Shutdown**: Handles Ctrl+C and system signals properly for clean exits with proper resource cleanup
- **Memory Management**: Includes garbage collection and efficient window extraction
- **Flexible Notifications**: Configurable notification system with retry mechanisms and error handling
- **Enhanced Reliability**: Improved error handling, connection recovery, and logging consistency

The standalone version is maintained for reference and research purposes, while the modular version (`fractalbot.py` + `fractal_trader.py`) is recommended for production use.

## Configuration

The system uses a **unified configuration architecture** that eliminates manual parameter transfer between optimization and live trading.

### Unified Strategy Configuration (`strategy_config_*.json`)

Both FractalBot and FractalTrader now load their parameters from a single, unified configuration file generated by the optimization framework. This ensures perfect consistency between signal generation and trade execution.

**File Location**: `bots/{symbol}/strategy_config_{symbol}.json`

**Example**: `bots/btc/strategy_config_btc.json`

```json
{
    "signal_parameters": {
        "dtw_method": "shapedtw",
        "feature_cols": ["close", "volume"],
        "window_size": 24,
        "top_n": 5,
        "proj_method": "top_match",
        "proj_top_n": 5,
        "descriptor_method": "RAW",
        "subsequence_window": 7
    },
    "trading_parameters": {
        "n_entry": 8,
        "use_sl": false,
        "n_tp": 1,
        "entry_agg_method": "max",
        "entry_base_offset_pct": 0.0152,
        "entry_spread_pct": 0.0182,
        "tp_agg_method": "max",
        "tp_base_offset_pct": 0.0490
    },
    "performance": {
        "train_objective_value": 21592.9,
        "validation_pnl_pct": 17721.7,
        "test_pnl_pct": 38606.4,
        "best_signal_config_key": "backtest_outputs_shapeDTW/predictions_data_...",
        "best_signal_validation_pnl": 15432.1
    }
}
```

### Configuration Sections

#### 1. Signal Parameters (`signal_parameters`)
Used by FractalBot for pattern matching and signal generation:

- **`dtw_method`**: DTW implementation to use (`'standard'` or `'shapedtw'`)
- **`feature_cols`**: Market features for pattern matching (e.g., `['close', 'volume']`)
- **`window_size`**: Length of patterns to match (e.g., `24` for 24-hour patterns)
- **`top_n`**: Number of best historical matches to find
- **`proj_method`**: How to aggregate projections (`'top_match'`, `'median'`, `'avg'`)
- **`proj_top_n`**: Number of matches to use for projection aggregation

**For ShapeDTW**:
- **`descriptor_method`**: Shape descriptor (`'RAW'`, `'PAA'`, `'PASSTHROUGH'`)
- **`subsequence_window`**: Local pattern window size (must be odd)

**For Standard DTW**:
- **`norm_method`**: Normalization method (`'zscore'`, `'minmax'`, `'peakvalley'`, etc.)

#### 2. Trading Parameters (`trading_parameters`)
Used by FractalTrader for trade execution:

- **`n_entry`**: Number of entry orders in the ladder
- **`n_tp`**: Number of take-profit orders
- **`entry_base_offset_pct`**: Base offset for entry price calculation
- **`entry_spread_pct`**: Spread percentage for entry ladder
- **`entry_agg_method`**: Aggregation method for entry price (`'max'`, `'min'`, `'median'`, `'mean'`)
- **`tp_base_offset_pct`**: Base offset for take-profit calculation
- **`tp_agg_method`**: Aggregation method for TP prices
- **`use_sl`**: Whether to use stop-loss orders
- **`sl_level_pct`**: Stop-loss percentage (if enabled)

#### 3. Performance Metrics (`performance`)
Records the optimization results for strategy comparison:

- **`train_objective_value`**: Training set performance
- **`validation_pnl_pct`**: Validation set performance
- **`test_pnl_pct`**: Final test set performance
- **`best_signal_config_key`**: Identifier of the best signal configuration
- **`best_signal_validation_pnl`**: Performance of the best signal config

### Automated Configuration Loading

Both components automatically load their respective parameters:

**FractalBot** (`run_fractalbot_*.py`):
```python
# Automatically loads signal_parameters from strategy_config_btc.json
strategy_config = load_strategy_config()
# Uses strategy_config['signal_parameters'] for analysis
```

**FractalTrader** (`run_trader_*.py`):
```python
# Automatically loads trading_parameters from strategy_config_btc.json
strategy_config = load_strategy_config()
# Passes strategy_config['trading_parameters'] to FractalTrader
```

### Strategy Deployment Workflow

1. **Run Optimizer**: Execute the DTW optimization framework to find best parameters
2. **Copy Configuration**: Copy `best_overall_config.json` to `bots/{symbol}/strategy_config_{symbol}.json`
3. **Automatic Loading**: Both FractalBot and FractalTrader automatically use the new parameters
4. **Performance Logging**: Both components log the strategy's performance metrics on startup

This unified approach ensures that:
- ✅ **No Manual Parameter Transfer**: Eliminates copy-paste errors
- ✅ **Perfect Reproducibility**: Signal generation exactly matches optimization conditions
- ✅ **Single Source of Truth**: One file defines the entire strategy
- ✅ **Easy Deployment**: New strategies deployed by copying a single file

## Integration with DTW Optimization Framework

The Fractal Trading System seamlessly integrates with the DTW optimization framework located in the `DTW/` directory. This integration provides a complete research-to-production pipeline:

### Optimization-to-Production Workflow

1. **Research Phase** (`DTW/` directory):
   - Run backtester notebooks to generate prediction datasets
   - Use `dtw_bot_config_single_level_optimization.py` or `dtw_bot_config_two_level_optimization.py`
   - Optimizer automatically identifies best signal configuration and trading parameters
   - Generates `best_overall_config.json` with complete strategy definition

2. **Deployment Phase** (this directory):
   - Copy `best_overall_config.json` to `bots/{symbol}/strategy_config_{symbol}.json`
   - Both FractalBot and FractalTrader automatically load their respective parameters
   - Strategy is immediately ready for live trading with optimal parameters

3. **Monitoring Phase**:
   - Both components log performance metrics on startup for verification
   - Strategy performance can be compared against optimization results
   - Easy to deploy new optimized strategies by replacing the config file

### Key Integration Features

- **Signal Configuration Parsing**: Optimizer automatically extracts signal parameters from prediction filenames
- **Best Configuration Detection**: Identifies which DTW method performed best during validation
- **Complete Strategy Output**: Generates unified configs ready for immediate deployment
- **Performance Tracking**: Records comprehensive metrics for strategy comparison
- **Zero Manual Transfer**: Eliminates the need to manually copy parameters between systems

This integration transforms the workflow from a manual, error-prone process to a fully automated pipeline from research to live trading.

## Signal File Format

FractalBot generates a JSON signal file which the FractalTrader consumes:

```json
{
    "timestamp_utc": "2025-06-23T18:56:30.729392",
    "symbol": "BTCUSDT",
    "trade_direction": "SHORT",
    "current_price_at_decision": 102484.02,
    "projected_paths_features": [
        {
            "min_pct": -0.0188,
            "max_pct": 0.0179,
            "final_pct": 0.0156,
            "avg_pct": 0.0167,
            "median_pct": 0.0171
        }
    ]
}
```

## Setup and Installation

### Prerequisites
1. Python 3.8+
2. Git
3. Binance Futures API credentials

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Fractal_Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Open `.env` and fill in your credentials:
```env
# Binance API Credentials (Required)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Telegram Bot Credentials (Optional - only needed if send_telegram_notifications=True)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_from_botfather
TELEGRAM_CHAT_ID=-100your_telegram_channel_id  # Note: Channel IDs start with -100

# Discord Bot Credentials (Optional - only needed if send_discord_notifications=True)
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id_here
```
**Important**: The `.env` file is listed in `.gitignore` and should never be committed to version control.

4. Prepare Historical Data:
   - Place your historical data CSV files in the `data/` directory
   - Ensure the `historical_data_path` in your `run_fractalbot_*.py` config points to the correct file

## Usage

### Running a Single Pair (e.g., BTC)

It is recommended to run each component in a separate terminal for clear log output.

1. **Start the Signal Generator (FractalBot)**:
```bash
# In your terminal
python ./bots/btc/run_fractalbot_btc.py
```
This bot will now run continuously, listening to the market data stream and generating a `daily_prediction_signal_btc.json` file on its schedule (at the start of a new UTC day). Charts will be saved to the `charts/` directory and can be viewed for analysis.

2. **Start the Trader (FractalTrader)**:
```bash
# In a new terminal
python ./bots/btc/run_trader_btc.py
```
This bot will start monitoring for the signal file and will execute trades when a new signal is generated.
Logs for this trader will be written to `bots/btc/fractal_trader_btc.log`.

## Operating Modes

The system has distinct modes for testing and live operation.

### FractalBot: Debug Mode vs. Live Mode

The FractalBot's behavior is controlled by the `debug` flag in its configuration (`run_fractalbot_*.py`):

- **Live Mode** (`'debug': False`): The bot runs continuously, connects to the Binance WebSocket, and generates signals based on kline timestamps for daily analysis. This is the standard production mode.
- **Debug Mode** (`'debug': True`): The bot runs continuously like Live Mode. On the first kline update, it immediately triggers a debug analysis (`Daily-Debug`), then continues running normally. Use `send_notifications_in_debug` to control whether notifications are sent during Debug Mode.

### FractalTrader: Paper Trading vs. Live Trading

The FractalTrader's execution mode is controlled by the `DEBUG_MODE` variable in its run script (`run_trader_*.py`):

- **Paper Trading Mode** (`DEBUG_MODE = True`): The trader runs continuously, watches for signal files, and simulates trades based on a live price feed. All actions are logged to `paper_trading_log.csv` without using real money. This is the recommended mode for strategy validation.

- **Live Trading Mode** (`DEBUG_MODE = False`): The trader runs continuously and executes real trades on your Binance account with real money. Use with caution.

### Adding a New Trading Pair

To add a new pair like ADAUSDT:

1. **Run Optimization for ADA**:
   - Use the DTW optimization framework to find the best strategy for ADAUSDT
   - This generates `best_overall_config.json` with optimized parameters

2. **Create a Directory**:
```bash
mkdir bots/ada
```

3. **Deploy Strategy Configuration**:
   - Copy `best_overall_config.json` to `bots/ada/strategy_config_ada.json`
   - This single file contains both signal and trading parameters

4. **Create `run_fractalbot_ada.py`**:
   - Copy `bots/btc/run_fractalbot_btc.py` to `bots/ada/`
   - Update the symbol and historical data path in the static configuration
   - The signal parameters will be loaded automatically from `strategy_config_ada.json`

5. **Create `run_trader_ada.py`**:
   - Copy `bots/btc/run_trader_btc.py` to `bots/ada/`
   - Update the `FractalTrader` instantiation with `symbol='ADAUSDT'`
   - The trading parameters will be loaded automatically from `strategy_config_ada.json`

6. **Run the New Pair**:
   Open two new terminals and run the new bot files just like you did for BTC.

**Benefits of the Unified Approach**:
- ✅ **Single File Deployment**: Only one configuration file to manage per pair
- ✅ **Guaranteed Consistency**: Signal generation exactly matches optimization conditions
- ✅ **No Manual Parameter Transfer**: Eliminates copy-paste errors between optimization and live trading
- ✅ **Performance Tracking**: Each configuration includes the optimization performance metrics

## File Management

### Chart Storage
- **Location**: All prediction charts are saved to the `charts/` directory (automatically created)
- **Naming**: Consistent filename based on prediction type:
  - `daily_prediction_chart.png` - Latest daily prediction
- **Overwriting**: Charts are overwritten on each new analysis, keeping only the latest prediction
- **Race Condition Protection**: File writing includes proper synchronization to prevent corrupted images in notifications

### Log Files
- **Location**: Each bot creates its own log file in its directory (e.g., `bots/btc/fractalbot_btc.log`)
- **Encoding**: UTF-8 encoding ensures compatibility with Unicode characters and emojis across all operating systems
- **Format**: Structured logging with timestamps and component identification

## Troubleshooting

### Common Issues

- **Signal files not generated**: Check the `fractalbot_*.log` file for errors. Verify data paths and API key permissions.
- **Trader not responding**: Ensure the `filename_to_watch` inside FractalTrader matches the signal filename being generated by FractalBot. Check that both bots are running for the same symbol.
- **Connection issues**: The ConnectionManager automatically handles most WebSocket disconnections and reconnections. Check logs for persistent connection errors or DNS resolution failures.
- **API errors**: Ensure your API keys are correct, have Futures trading enabled in Binance, and are not restricted by IP if applicable.
- **Import errors**: Run the scripts from the project's root directory (`Fractal_Bot/`) to ensure the Python path is set correctly.

### Windows-Specific Issues

- **Unicode/Emoji errors**: The system now uses UTF-8 encoding for all log files to prevent `UnicodeEncodeError` when writing emojis or special characters
- **Path separators**: The system handles both forward and backward slashes automatically
- **Console display**: While emojis in logs may not display correctly in some Windows terminals, they will be properly saved to log files

### Performance and Reliability

- **Resource cleanup**: If you experience hanging processes, the improved shutdown handling should resolve most issues. Use Ctrl+C for graceful termination.
- **Memory management**: The system includes garbage collection and efficient data handling for long-running operations
- **File corruption**: Chart generation includes proper file flushing and timing to prevent corrupted images in notifications
- **Environment variables**: If you get credential errors, ensure your `.env` file is in the project root and contains all required variables for your enabled notification services.

### Logging System

The system uses Python's standard logging module with the following features:
- **Dual output**: Logs are written to both console and file simultaneously
- **UTF-8 encoding**: Full Unicode support for international characters and emojis
- **Structured format**: Consistent log formatting with component identification
- **Error handling**: Comprehensive error logging with stack traces for debugging 

==================================================

## FILE 2: run_fractalbot_btc.py
**Path:** Fractal_Bot\bots\btc\run_fractalbot_btc.py
**Type:** Source Code (.py)
**Size:** 178 lines, 7365 bytes
**Modified:** 2025-07-07T11:32:12.611478
==================================================
import sys
import os
import logging
from dotenv import load_dotenv

# Add the project root to the Python path to allow imports from 'src' and root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# After adding project_root to sys.path, also add the 'src' directory
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Load environment variables from .env file
load_dotenv(os.path.join(project_root, '.env'))

# --- Load ALL credentials from environment variables ---
API_KEY = os.getenv("BINANCE_API_KEY")  # This will be None if not set
API_SECRET = os.getenv("BINANCE_API_SECRET")  # This will be None if not set
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_FRACTAL_TRADER")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID_DAILY")  # Unified Discord Channel ID

# --- Import bot logic from the src package ---
try:
    from src.fractalbot import FractalBot
    from src.telegram_client import TelegramClient
    from src.discord_client import DiscordClient
except ImportError as e:
    print(f"FATAL ERROR: Could not import required modules from src: {e}")
    print(f"Current Python path: {sys.path}")
    print(f"Project root: {project_root}")
    sys.exit(1)

# --- NEW: Unified Logger Setup ---
log_file_path = os.path.join(os.path.dirname(__file__), 'fractalbot_btc.log')
log_formatter = logging.Formatter('%(asctime)s - [BTC-FRACTALBOT] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Get the root logger (this is what all logging.info() calls use)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Clear any existing handlers to prevent duplicates
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Create Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

# --- THE FIX IS HERE ---
# Create File Handler with explicit UTF-8 encoding (append mode to preserve logs)
file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
# --- END OF FIX ---
file_handler.setFormatter(log_formatter)

# Add both handlers to the root logger
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

# Create a logger object for the bot (this will inherit from root)
logger = logging.getLogger('BTC-FRACTALBOT')
# --- END NEW LOGGER SETUP ---

# --- Load Unified Strategy Configuration ---
import json

def load_strategy_config():
    """Load the unified strategy configuration from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'strategy_config_btc.json')
    
    try:
        with open(config_path, 'r') as f:
            strategy_config = json.load(f)
        logger.info(f"Successfully loaded strategy configuration from {config_path}")
        logger.info(f"Strategy Performance Summary:")
        logger.info(f"  - Train PnL: {strategy_config['performance']['train_objective_value']:.1f}%")
        logger.info(f"  - Validation PnL: {strategy_config['performance']['validation_pnl_pct']:.1f}%")
        logger.info(f"  - Test PnL: {strategy_config['performance']['test_pnl_pct']:.1f}%")
        logger.info(f"  - Signal Config: {strategy_config['performance']['best_signal_config_key']}")
        return strategy_config
    except FileNotFoundError:
        logger.error(f"Strategy configuration file not found at {config_path}")
        logger.error("Please ensure the optimizer has been run and the config file is in the correct location.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in strategy configuration file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading strategy configuration: {e}")
        sys.exit(1)

# Load the strategy configuration
strategy_config = load_strategy_config()

# --- Build the Bot's Full Configuration ---
# Combine static settings with loaded signal parameters
BTC_BOT_CONFIG = {
    'symbol': 'BTCUSDT',
    'interval': '1h',
    'lookback': 700,
    'historical_data_path': os.path.join(project_root, 'data', '1h_2017-08-17_2025-06-20.csv'),
    
    # --- Main Control Flags ---
    'debug': False,  # Set to True to enable debug logging and behavior
    'send_notifications_in_debug': False, # Set to False to run quietly

    # --- Optional heartbeat logging ---
    # When True, FractalBot logs every closed 1-minute candle (O/H/L/C) to help verify the spot feed.
    'log_1m_candles': True,

    # --- Notification Control Flags ---
    'send_discord_notifications': False,  # Set to True to enable Discord notifications
    'send_telegram_notifications': True,  # Set to True to enable Telegram notifications
    
    # --- Parameters needed for legacy plotting ---
    'num_entry_orders': 2,
    'num_tp_orders': 7,

    # --- Load the dynamic analysis parameters from the unified config file ---
    'daily': strategy_config['signal_parameters'],
    
    # --- Store trading parameters for future use (FractalTrader integration) ---
    'trading_parameters': strategy_config['trading_parameters'],
    'strategy_performance': strategy_config['performance']
    
    # NOTE: Weekly and monthly analysis are disabled in fractalbot.py
    # Only daily analysis is currently active
}

if __name__ == "__main__":
    logger.info("Starting BTC FractalBot...")
    
    # --- Instantiate Clients ---
    telegram_client = None
    if BTC_BOT_CONFIG.get('send_telegram_notifications'):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logger.error("Telegram notifications enabled but credentials not found in .env file.")
            sys.exit(1)
        telegram_client = TelegramClient(bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

    discord_client = None
    if BTC_BOT_CONFIG.get('send_discord_notifications'):
        if not DISCORD_BOT_TOKEN or not DISCORD_CHANNEL_ID:
            logger.error("Discord notifications enabled but credentials not found in .env file.")
            sys.exit(1)
        discord_client = DiscordClient(bot_token=DISCORD_BOT_TOKEN, chat_id=DISCORD_CHANNEL_ID)
    
    try:
        # --- MODIFIED: Inject the new dependencies ---
        bot_instance = FractalBot(
            config=BTC_BOT_CONFIG,
            logger=logger,  # Pass the standard logger instance
            telegram_client=telegram_client,
            discord_client=discord_client, # Pass the discord client
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        
        logger.info("FractalBot instance created successfully. Starting bot...")
        bot_instance.run()
        logger.info("FractalBot finished running.")
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down gracefully...")
        if 'bot_instance' in locals():
            bot_instance.stop()
        # Force exit to prevent hanging on uncleaned asyncio tasks from binance library
        import os
        os._exit(0)
    except Exception as e:
        # Use the logger's error method
        logger.error(f"Critical error with BTC FractalBot: {e}")
        sys.exit(1)

==================================================

## FILE 3: fractalbot.py
**Path:** Fractal_Bot\src\fractalbot.py
**Type:** Source Code (.py)
**Size:** 1637 lines, 80593 bytes
**Modified:** 2025-07-07T15:56:19.905097
==================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from numpy.lib.stride_tricks import as_strided
import time
import os
import urllib.parse
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- ADD THESE IMPORTS ---
from connection_manager import ConnectionManager
from discord_client import DiscordClient
from telegram_client import TelegramClient
from notification_manager import send_notification
import matplotlib.dates as mdates
from binance.client import Client
# --- REMOVED: from binance import ThreadedWebsocketManager ---
import matplotlib
matplotlib.use('Agg')
import discord
from discord.ext import commands
import asyncio
import threading
from numba import njit
import concurrent.futures
import gc
import json
import sys

# --- CORRECTED DTW IMPORT ---
try:
    # Use absolute import for DTW.py in the same directory
    from DTW import dtwClc
except ImportError:
    logging.warning("DTW module not found or dtwClc function not available. DTW functionality may be limited.")
    def dtwClc(*args, **kwargs):
        raise NotImplementedError("DTW function not available")

# --- NEW: Import ShapeDTW ---
try:
    from shapeDTW import shape_dtw_distance_mv
except ImportError:
    logging.warning("shapeDTW module not found. ShapeDTW will be unavailable.")
    def shape_dtw_distance_mv(*args, **kwargs):
        raise NotImplementedError("shape_dtw_distance_mv function is not available")

def get_binance_data(symbol='BTCUSDT', interval='1h', lookback_periods=1000):
    """
    Fetch candle data from Binance API, ensuring only COMPLETE candles are returned.

    This function works by setting the API `endTime` to the start time of the
    current, in-progress candle. The API then returns candles with an open time
    before or at this timestamp, effectively excluding the live candle.

    Args:
        symbol (str): Trading pair (e.g., 'BTCUSDT').
        interval (str): Candle timeframe (e.g., '1h', '4h', '1d').
        lookback_periods (int): The number of closed candles to retrieve.

    Returns:
        pd.DataFrame: A DataFrame with the requested number of complete candles.
                      Returns an empty DataFrame on error.
    """
    client = Client() # Initialize client inside function, or pass it if you prefer
    
    # --- Correct and Simplified Time Calculation ---
    now = datetime.utcnow()
    
    # Floor the current time to the beginning of the current candle's interval
    start_of_current_candle = None
    if interval.endswith('h'):
        # For any hourly interval (1h, 4h, etc.), just zero out the smaller units
        start_of_current_candle = now.replace(minute=0, second=0, microsecond=0)
    elif interval.endswith('d'):
        # For daily intervals
        start_of_current_candle = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif interval.endswith('m'):
        # For minute intervals
        minutes_in_interval = int(interval[:-1])
        start_of_current_candle = now.replace(second=0, microsecond=0)
        start_of_current_candle -= timedelta(minutes=now.minute % minutes_in_interval)
    else:
        logging.error(f"Unsupported interval '{interval}' for time calculation in get_binance_data.")
        return pd.DataFrame()

    # The API's endTime should be the exact start time of the current candle.
    # Convert this to a millisecond timestamp.
    end_time_ms = int(start_of_current_candle.timestamp() * 1000)
    
    try:
        # Use get_klines with endTime to exclude the current incomplete candle
        klines = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=lookback_periods, # Request `lookback_periods` before `endTime_ms`
            endTime=end_time_ms
        )
        
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        if df.empty:
            logging.warning(f"No data returned from Binance for {symbol} with interval {interval}.")
            return pd.DataFrame()

        # Convert numeric columns
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])
        
        # Convert timestamp to datetime and set as index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Final check: Ensure the last candle received is indeed a completed one
        # (Sometimes Binance might still return an incomplete one if query is at exact boundary)
        if not df.empty and df.index[-1] >= start_of_current_candle:
            logging.warning("API returned an incomplete candle despite `endTime`. Removing it.")
            # Filter out any candle that opens at or after the `start_of_current_candle`
            df = df[df.index < start_of_current_candle]
            
        logging.info(f"Fetched {len(df)} data points from Binance for {symbol}")
        return df[numeric_columns] # Return only desired numeric columns
    
    except Exception as e:
        logging.error(f"Error fetching data from Binance in get_binance_data: {e}", exc_info=True)
        return pd.DataFrame()



def load_historical_data(filepath, start_date=None, end_date=None):
    """
    Loads historical data from a CSV file.
    """
    try:
        df = pd.read_csv(filepath)
        
        # Try to parse the timestamp column with mixed format support
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
            df.set_index('timestamp', inplace=True)
        elif 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='mixed')
            df.set_index('Timestamp', inplace=True)
        else:
            # Assume first column is timestamp
            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='mixed')
            df.set_index(df.columns[0], inplace=True)
        
        # Filter by date range if provided
        if start_date:
            df = df[df.index >= start_date]
        if end_date:
            df = df[df.index <= end_date]
        
        return df
    except Exception as e:
        logging.error(f"Error loading historical data from {filepath}: {e}")
        return pd.DataFrame()

def extract_windows_efficiently(data, window_size):
    """
    Efficiently extracts sliding windows from data using numpy stride tricks.
    """
    if len(data) < window_size:
        return np.array([])
    
    # Convert to numpy array if it's a pandas DataFrame/Series
    if hasattr(data, 'values'):
        values = data.values
    else:
        values = np.array(data)
    
    # Handle multi-dimensional data
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    
    n_rows, n_cols = values.shape
    n_windows = n_rows - window_size + 1
    
    if n_windows <= 0:
        return np.array([])
    
    # Use stride tricks to create sliding windows
    strides = (values.strides[0], values.strides[0], values.strides[1])
    windows = as_strided(values, 
                        shape=(n_windows, window_size, n_cols),
                        strides=strides)
    
    return windows

def normalize_window_numpy(window_data, norm_method='zscore'):
    """
    Normalizes a numpy array window using the specified method.
    Returns None if normalization fails.
    """
    if window_data.size == 0:
        return None
    
    # Ensure window_data is float32 for Numba compatibility later
    window_data = np.asarray(window_data, dtype=np.float32)

    # Reshape 1D arrays to 2D (time x 1 feature) for consistent processing
    if window_data.ndim == 1:
        window_data = window_data.reshape(-1, 1)

    # Check for minimum length required by some methods
    if window_data.shape[0] < 2 and norm_method in ['returns', 'logreturns', 'voladjusted', 'firstdiff', 'slope', 'ddtw', 'peakvalley']:
        # logging.debug(f"Window too short ({window_data.shape[0]}) for norm_method '{norm_method}'.")
        return None # Return None if window is too short for method

    normalized_cols = []
    n_features = window_data.shape[1]

    try:
        # Process each feature column independently if needed, otherwise apply broadly
        for j in range(n_features):
            col = window_data[:, j]
            norm_col = None # Initialize for current column

            if norm_method == 'startpoint':
                first_value = col[0]
                norm_col = (col - first_value) / np.maximum(np.abs(first_value), 1e-9)
            elif norm_method == 'zscore':
                mean_val = np.mean(col)
                std_val = np.std(col)
                norm_col = (col - mean_val) / np.maximum(std_val, 1e-9)
            elif norm_method == 'minmax':
                min_val = np.min(col)
                max_val = np.max(col)
                range_val = max_val - min_val
                norm_col = (col - min_val) / np.maximum(range_val, 1e-9)
            elif norm_method == 'hampel':
                median_val = np.median(col)
                mad_val = np.median(np.abs(col - median_val))
                norm_col = (col - median_val) / np.maximum(mad_val, 1e-9) / 1.4826 # Standard Hampel
            elif norm_method == 'returns':
                if len(col) < 2: return None
                returns = np.diff(col) / np.maximum(np.abs(col[:-1]), 1e-9)
                norm_col = np.concatenate(([0], returns))
            elif norm_method == 'logreturns':
                if len(col) < 2 or np.any(col <= 1e-9): return None
                returns = np.diff(np.log(col))
                norm_col = np.concatenate(([0], returns))
            elif norm_method == 'voladjusted':
                 if len(col) < 2 or np.any(col <= 1e-9): return None
                 returns = np.diff(np.log(col))
                 lookback_vol = min(20, len(returns))
                 if lookback_vol < 1: return None
                 vol = np.std(returns[-lookback_vol:])
                 norm_col = np.concatenate(([0], returns / np.maximum(vol, 1e-9)))
            # NEW: PeakValley Normalization
            elif norm_method == 'peakvalley':
                if len(col) < 3:
                    logging.warning("Window too short for peakvalley normalization, using zscore fallback.")
                    mean_val = np.mean(col)
                    std_val = np.std(col)
                    norm_col = (col - mean_val) / np.maximum(std_val, 1e-9) # Fallback to zscore
                else:
                    diff = np.diff(col)
                    peaks = np.where((diff[:-1] > 0) & (diff[1:] < 0))[0] + 1
                    valleys = np.where((diff[:-1] < 0) & (diff[1:] > 0))[0] + 1
                    extremes = np.concatenate((peaks, valleys))
                    
                    if len(extremes) > 0:
                        ref = np.mean(col[extremes])
                        std_ref = np.std(col[extremes])
                        norm_col = (col - ref) / np.maximum(std_ref, 1e-9)
                    else: # Fallback if no distinct peaks/valleys found (e.g., monotonic or flat)
                        logging.debug("No distinct peaks/valleys found for peakvalley, using zscore fallback.")
                        mean_val = np.mean(col)
                        std_val = np.std(col)
                        norm_col = (col - mean_val) / np.maximum(std_val, 1e-9)
            # Add other normalization methods here if desired
            # elif norm_method == 'firstdiff':
            #     diff = np.diff(col)
            #     norm_col = np.concatenate(([0], diff))
            # ... and so on for other methods like 'slope', 'ddtw', 'logscale', etc.

            else:
                logging.warning(f"Unknown normalization method: {norm_method}. Using zscore.")
                mean_val = np.mean(col)
                std_val = np.std(col)
                norm_col = (col - mean_val) / np.maximum(std_val, 1e-9)
            
            if norm_col is None or not np.all(np.isfinite(norm_col)):
                logging.error(f"Normalization failed for method '{norm_method}', feature index {j}.")
                return None # Indicate failure for the entire window

            normalized_cols.append(norm_col)

        if not normalized_cols: # This might happen if all columns failed or no features
            return None

        window_norm = np.stack(normalized_cols, axis=-1)
        
        # Ensure C-contiguity and float32 dtype
        return np.ascontiguousarray(window_norm, dtype=np.float32)

    except Exception as e:
        logging.error(f"Error in normalize_window_numpy ({norm_method}): {e}", exc_info=True)
        return None

def _find_matches_with_standard_dtw(recent_data, historical_data, feature_cols, window_size, top_n, norm_method, debug_io_flag, min_separation_hours=None):
    """Find best matching historical patterns using the batched Numba CPU DTW (dtwClc)."""

    if historical_data is None or historical_data.empty:
        logging.error("Historical data is missing, cannot find matches.")
        return pd.DataFrame()

    required_cols = set(feature_cols + ['open_time'])
    if not required_cols.issubset(recent_data.columns) or not required_cols.issubset(historical_data.columns):
        logging.error(f"Data is missing required columns. Need: {required_cols}")
        return pd.DataFrame()

    if len(recent_data) < window_size:
        logging.warning(f"Recent data length ({len(recent_data)}) is less than window size ({window_size}).")
        return pd.DataFrame()

    # --- 1. Prepare Current Window ---
    current_window_df = recent_data.tail(window_size)
    if debug_io_flag:
        logging.info("\n--- DEBUG I/O: Current Pattern Input ---")
        log_df = current_window_df[['open_time'] + feature_cols].copy()
        log_df['open_time'] = log_df['open_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Current Pattern (last {window_size} candles):\n{log_df.to_string()}")
        logging.info("--------------------------------------\n")

    current_window_data = current_window_df[feature_cols].values
    current_normalized = normalize_window_numpy(current_window_data, norm_method)
    if current_normalized is None:
        logging.error(f"Failed to normalize the current window with method '{norm_method}'.")
        return pd.DataFrame()

    # --- 2. Prepare ALL Historical Windows ---
    all_windows_raw = extract_windows_efficiently(historical_data[feature_cols], window_size)
    if all_windows_raw.size == 0:
        logging.error("Failed to extract any historical windows.")
        return pd.DataFrame()

    all_windows_norm_list = []
    valid_indices = []
    for i, hist_window_data in enumerate(all_windows_raw):
        normalized_hist = normalize_window_numpy(hist_window_data, norm_method)
        if normalized_hist is not None:
            all_windows_norm_list.append(normalized_hist)
            valid_indices.append(i)

    if not all_windows_norm_list:
        logging.error("Failed to normalize any historical windows.")
        return pd.DataFrame()

    all_windows_norm = np.stack(all_windows_norm_list, axis=0)
    all_windows_norm = np.ascontiguousarray(all_windows_norm, dtype=np.float32)

    # --- 3. Call Batched DTW Correctly ---
    logging.info(f"Comparing current window against {len(all_windows_norm)} valid historical windows...")
    start_time_dtw = time.time()
    
    n_historical = all_windows_norm.shape[0]
    lenSeq = current_normalized.shape[0]
    n_features = current_normalized.shape[1]
    
    current_normalized_3d = np.ascontiguousarray(current_normalized.reshape(1, lenSeq, n_features), dtype=np.float32)
    INDList_np = np.array([(0, i) for i in range(n_historical)], dtype=np.int32)
    distances = np.empty(n_historical, dtype=np.float64)

    dtwClc(
        current_normalized_3d,  # seq
        all_windows_norm,       # trg
        lenSeq,                 # lenEachSeq
        lenSeq,                 # lenEachTrg
        n_features,             # n_features
        n_historical,           # lenDTW
        INDList_np,             # INDList
        distances               # dtw (output array)
    )
    
    logging.info(f"DTW calculation finished in {time.time() - start_time_dtw:.2f} seconds.")

    # --- 4. Process Results ---
    matches = []
    for i, dist in enumerate(distances):
        if np.isfinite(dist):
            original_index = valid_indices[i]
            matches.append({
                'match_start_idx': original_index,
                'match_end_idx': original_index + window_size - 1,
                'similarity_score': dist
            })

    if not matches:
        logging.warning("No finite similarity scores found after DTW.")
        return pd.DataFrame()

    matches_df = pd.DataFrame(matches).sort_values('similarity_score', ascending=True)

    # --- 5. Apply Time Separation Filter ---
    best_matches = []
    selected_times = set()
    min_delta = timedelta(hours=(min_separation_hours if min_separation_hours is not None else window_size * 2))

    for _, match in matches_df.iterrows():
        match_end_time = historical_data.iloc[int(match['match_end_idx'])]['open_time']
        
        is_separated = all(abs(match_end_time - t) > min_delta for t in selected_times)
        
        if is_separated:
            match['match_start'] = historical_data.iloc[int(match['match_start_idx'])]['open_time']
            match['match_end'] = match_end_time
            best_matches.append(match)
            selected_times.add(match_end_time)
            if len(best_matches) >= top_n:
                break

    if not best_matches:
        logging.warning("No matches found after applying time separation filter.")
        return pd.DataFrame()

    return pd.DataFrame(best_matches)

def _find_matches_with_shapedtw(recent_data, historical_data, feature_cols, window_size, top_n, descriptor_method, subsequence_window, debug_io_flag, min_separation_hours=None):
    """Finds best matching historical patterns using shapeDTW."""

    if historical_data is None or historical_data.empty:
        logging.error("Historical data is missing for ShapeDTW.")
        return pd.DataFrame()

    if len(recent_data) < window_size:
        logging.warning(f"Recent data length ({len(recent_data)}) is less than window size ({window_size}).")
        return pd.DataFrame()

    # 1. Prepare Current and Historical Windows (RAW DATA)
    current_window_df = recent_data.tail(window_size)
    current_window_data = current_window_df[feature_cols].values
    all_windows_raw = extract_windows_efficiently(historical_data[feature_cols], window_size)
    
    if all_windows_raw.size == 0:
        logging.error("Failed to extract historical windows for ShapeDTW.")
        return pd.DataFrame()

    # 2. Call ShapeDTW
    logging.info(f"Comparing current window against {len(all_windows_raw)} raw historical windows using ShapeDTW...")
    start_time_dtw = time.time()
    
    current_window_f32 = np.ascontiguousarray(current_window_data, dtype=np.float32)
    all_windows_f32 = np.ascontiguousarray(all_windows_raw, dtype=np.float32)

    distances = shape_dtw_distance_mv(
        query=current_window_f32,
        templates=all_windows_f32,
        subsequence_window=subsequence_window,
        descriptor_method=descriptor_method
    )
    logging.info(f"ShapeDTW finished in {time.time() - start_time_dtw:.2f} seconds.")
    
    # 3. Process and Filter Results (This logic is reusable)
    matches = []
    for i, dist in enumerate(distances):
        if np.isfinite(dist):
            matches.append({'match_start_idx': i, 'match_end_idx': i + window_size - 1, 'similarity_score': dist})

    if not matches:
        return pd.DataFrame()

    matches_df = pd.DataFrame(matches).sort_values('similarity_score')

    best_matches = []
    selected_times = set()
    min_delta = timedelta(hours=(min_separation_hours if min_separation_hours is not None else window_size * 2))

    for _, match in matches_df.iterrows():
        match_end_idx = int(match['match_end_idx'])
        match_end_time = historical_data.iloc[match_end_idx]['open_time']
        
        if all(abs(match_end_time - t) > min_delta for t in selected_times):
            match['match_start'] = historical_data.iloc[int(match['match_start_idx'])]['open_time']
            match['match_end'] = match_end_time
            best_matches.append(match)
            selected_times.add(match_end_time)
            if len(best_matches) >= top_n:
                break
    
    return pd.DataFrame(best_matches) if best_matches else pd.DataFrame()

def find_best_fractal_matches(recent_data, historical_data, analysis_config, debug_io_flag=False):
    """
    Dispatcher function that selects the correct DTW implementation based on config.
    """
    # Default to 'standard' if the key is missing, for backward compatibility
    dtw_method = analysis_config.get('dtw_method', 'standard').lower()
    
    logging.info(f"Dispatching to DTW method: '{dtw_method}'")
    
    # Common parameters for both methods
    params = {
        'recent_data': recent_data,
        'historical_data': historical_data,
        'feature_cols': analysis_config.get('feature_cols'),
        'window_size': analysis_config.get('window_size'),
        'top_n': analysis_config.get('top_n'),
        'debug_io_flag': debug_io_flag
    }

    if dtw_method == 'shapedtw':
        # Add ShapeDTW-specific parameters
        params['descriptor_method'] = analysis_config.get('descriptor_method', 'RAW')
        params['subsequence_window'] = analysis_config.get('subsequence_window', 5)
        return _find_matches_with_shapedtw(**params)
        
    elif dtw_method == 'standard':
        # Add standard DTW-specific parameters
        params['norm_method'] = analysis_config.get('norm_method', 'zscore')
        return _find_matches_with_standard_dtw(**params)
        
    else:
        logging.error(f"Unknown dtw_method '{dtw_method}'. Must be 'standard' or 'shapedtw'.")
        return pd.DataFrame()

# --- LEGACY PLOTTING FUNCTION FROM STANDALONE BOT ---
def plot_multiple_matches(matches, recent_data, historical_data, window_size, forward_periods,
                         prediction_type='Daily',
                         num_entry_orders=2, num_tp_orders=4,
                         projection_method='median', projection_top_n=5,
                         debug_io_flag=False, feature_cols=None):
    """
    Plot multiple matches with projections, ensuring all start at the anchor point
    with correct initial x-axis spacing.
    Plots relative changes for pattern matching and absolute prices for projections.
    Calculates and returns trade recommendations based on the projection.
    *** Uses Matplotlib's default color cycle for match colors. ***
    """
    # Default feature_cols if not provided, for logging robustness
    _feature_cols = feature_cols if feature_cols is not None else ['open', 'high', 'low', 'close', 'volume']

    # --- Define plot_markers_on_line helper function ---
    def plot_markers_on_line(ax, line_dates, line_values, tick_locs_num, color, marker_style, marker_size):
        """Helper function to plot markers on a line only within its date range."""
        if line_dates.empty or len(line_dates) < 2:
            return  # Not enough data to create a range

        # Get the date range of the line
        line_dates_num = mdates.date2num(line_dates)
        min_date_num, max_date_num = line_dates_num[0], line_dates_num[-1]

        # Filter ticks to be within the line's range
        filtered_ticks_num = [tick for tick in tick_locs_num if min_date_num <= tick <= max_date_num]

        if not filtered_ticks_num:
            return  # No ticks fall within this line's range

        # Interpolate the y-values at the precise, filtered tick locations
        marker_values = np.interp(filtered_ticks_num, line_dates_num, line_values)

        # Plot markers
        ax.plot(filtered_ticks_num, marker_values, marker=marker_style,
                markersize=marker_size, color=color, alpha=0.9,
                linestyle='', markerfacecolor=color, markeredgecolor='white',
                markeredgewidth=1.5, zorder=15)

    # --- Premium Styling Variables ---
    plt.style.use('seaborn-whitegrid')  # Keep this or similar base style
    golden_ratio = 1.618
    accent_colors = ['#c62828', '#ad1457', '#6a1b9a', '#4527a0', '#283593', '#1565c0', '#0277bd', '#00695c', '#2e7d32', '#558b2f', '#827717', '#f57c00', '#ef6c00', '#d84315']
    bg_color = '#fefefe'  # For figure facecolor
    chart_bg = '#fbfbfb'  # For axes facecolor

    top_matches = matches  # Rename for internal consistency

    if top_matches.empty:
        logging.warning("No matches provided to plot.")
        return None, None, [], [], []

    if forward_periods is None:
        forward_periods = window_size
        logging.warning("forward_periods not provided, defaulting to window_size.")

    # --- Calculate time string and interval timedelta ---
    time_str = f"{forward_periods} periods"
    interval_timedelta = pd.Timedelta(hours=1) # Default
    try:
        if len(recent_data) >= 2:
            # Use diff().median() for robustness against missing candles
            interval_seconds = recent_data['open_time'].diff().dropna().median().total_seconds()
            if interval_seconds > 0:
                interval_timedelta = pd.Timedelta(seconds=interval_seconds)
                total_projection_seconds = interval_seconds * forward_periods
                projection_days = int(total_projection_seconds // (24 * 3600))
                projection_hours = int((total_projection_seconds % (24 * 3600)) // 3600)

                if projection_days > 0 and projection_hours > 0: time_str = f"{projection_days}d, {projection_hours}h"
                elif projection_days > 0: time_str = f"{projection_days} days"
                elif projection_hours > 0: time_str = f"{projection_hours} hours"
                else:
                    projection_minutes = int(total_projection_seconds // 60)
                    time_str = f"{projection_minutes} min" if projection_minutes > 0 else f"{int(total_projection_seconds)} sec"
                logging.debug(f"Calculated interval: {interval_timedelta}, Projection time string: {time_str}")
            else:
                logging.warning("Could not infer positive interval timedelta, defaulting to 1 hour.")
        else:
            logging.warning("Not enough recent data to calc interval, defaulting interval timedelta to 1 hour.")
    except Exception as e:
        logging.error(f"Error calculating time interval: {e}. Using default.", exc_info=True)

    title = f'Top {len(top_matches)} {prediction_type} Fractal Matches with {time_str} Projection'

    fig = None
    try:
        # --- Figure and Axes Setup with Premium Styling for a SINGLE plot (ax3) ---
        fig_height_main = 10
        fig_width_main = fig_height_main * golden_ratio
        fig = plt.figure(figsize=(fig_width_main, fig_height_main), facecolor=bg_color, edgecolor='none')
        fig.patch.set_facecolor(bg_color)

        # ax3 will be the only subplot on this figure
        ax3 = fig.add_subplot(111, facecolor=chart_bg)  # Use 111 for a single subplot

        # --- End Figure and Axes Setup ---

        # --- Get Current Pattern Data ---
        first_match = top_matches.iloc[0]
        # Get the integer index directly from the DataFrame
        current_start_idx = first_match.current_start_idx

        if current_start_idx + window_size > len(recent_data):
            logging.error(f"Window size {window_size} exceeds available recent_data length from index {current_start_idx}.")
            if fig is not None and plt.fignum_exists(fig.number): plt.close(fig) # Close figure on error
            return None, None, [], [], []

        current_data = recent_data.iloc[current_start_idx : current_start_idx + window_size]
        if current_data.empty:
            logging.error("Failed to extract current pattern data.")
            if fig is not None and plt.fignum_exists(fig.number): plt.close(fig) # Close figure on error
            return None, None, [], [], []

        # --- Identify Anchor Point ---
        current_final_price = current_data['close'].iloc[-1]
        current_final_date = current_data['open_time'].iloc[-1] # Time of the last candle in pattern
        projection_period_start_time = current_final_date + interval_timedelta
        logging.info(f"Anchor Point: Price={current_final_price:.4f}, Time={projection_period_start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        # --- Plot Pattern (Top Panel) ---
        search_start_idx = max(0, current_start_idx - window_size)
        search_window = recent_data.iloc[search_start_idx : current_start_idx]
        current_base = current_data['close'].iloc[0]; current_base = max(current_base, 1e-9) # Avoid zero division
        search_rel = (search_window['close'] / current_base - 1) if not search_window.empty else pd.Series(dtype=float)
        current_rel = (current_data['close'] / current_base - 1)

        all_projections_data = [] # Stores dicts for each match's full projection path
        all_projected_prices_for_ylim = []

        # --- BOT DEBUG I/O: Log matched patterns and their historical projections ---
        if debug_io_flag:
            logging.info("\n--- BOT DEBUG I/O: Matched Patterns & Historical Projections ---")

        # --- Loop Through Matches ---
        for i, match in enumerate(top_matches.itertuples(index=False)):
            try:
                # Find historical start index robustly
                hist_start_indices = historical_data[historical_data['open_time'] == match.match_start].index
                if hist_start_indices.empty:
                    logging.warning(f"M{i+1}: Hist start time {match.match_start} not found. Skipping."); continue
                hist_start_idx = hist_start_indices[0]

                if hist_start_idx + window_size > len(historical_data): logging.warning(f"M{i+1}: Hist data too short for pattern end. Skipping."); continue

                hist_pattern = historical_data.iloc[hist_start_idx : hist_start_idx + window_size]
                if hist_pattern.empty: logging.warning(f"M{i+1}: Failed to extract hist pattern. Skipping."); continue

                # --- Calculate Future Projection Path ---
                hist_pattern_end_idx = hist_start_idx + window_size - 1
                hist_forward_start_idx = hist_pattern_end_idx + 1
                # Ensure we don't request more future points than exist in historical data
                max_available_forward = len(historical_data) - hist_forward_start_idx
                actual_forward_periods = min(forward_periods, max_available_forward)
                forward_end_idx = hist_forward_start_idx + actual_forward_periods # Adjusted end index

                # --- BOT DEBUG I/O: Log the matched pattern and its forward data ---
                if debug_io_flag:
                    log_cols_debug = [col for col in _feature_cols if col in hist_pattern.columns]
                    logging.info(f"\n--- Match #{i+1} (Score: {match.similarity_score:.4f}) ---")
                    logging.info("Historical Matched Pattern:")
                    # --- MODIFICATION FOR MATCHED PATTERN ---
                    temp_log_df_match = hist_pattern[['open_time'] + log_cols_debug].copy()
                    temp_log_df_match['open_time'] = temp_log_df_match['open_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    logging.info(f"\n{temp_log_df_match.to_string()}")
                    # --- END MODIFICATION ---

                    # Also log the forward data that will be used for projection
                    hist_forward_df = historical_data.iloc[hist_forward_start_idx : forward_end_idx]
                    if not hist_forward_df.empty:
                        logging.info("Historical Forward Data (for projection):")
                        # --- MODIFICATION FOR HISTORICAL FORWARD ---
                        log_cols_fwd_debug = [col for col in _feature_cols if col in hist_forward_df.columns] # Use _feature_cols
                        temp_log_df_hist_fwd = hist_forward_df[['open_time'] + log_cols_fwd_debug].copy()
                        temp_log_df_hist_fwd['open_time'] = temp_log_df_hist_fwd['open_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
                        logging.info(f"\n{temp_log_df_hist_fwd.to_string()}")
                        # --- END MODIFICATION ---
                    else:
                        logging.info("Historical Forward Data: (Not available or not enough data)")
                # --- End BOT DEBUG I/O ---

                # Initialize lists for this match's plot *starting with the anchor*
                plot_dates_this_match = [projection_period_start_time]
                plot_prices_this_match = [current_final_price]
                proj_prices_future_for_ylim = [] # Separate list for future prices needed for Y-lim calc

                # Try to calculate and append future points only if actual_forward_periods > 0
                if actual_forward_periods > 0:
                    hist_forward = historical_data.iloc[hist_forward_start_idx : forward_end_idx] # Use adjusted end index
                    if not hist_forward.empty:
                        hist_end_price = hist_pattern['close'].iloc[-1]
                        if hist_end_price > 1e-9: # Check for non-zero price
                            # Calculate future prices relative to historical end price
                            hist_forward_pct_changes = [(p / hist_end_price) - 1 for p in hist_forward['close']]
                            proj_prices_future = [current_final_price * (1 + pct_change) for pct_change in hist_forward_pct_changes]

                            # --- ### CORRECTED DATE CALCULATION ### ---
                            # Generate future dates with consistent spacing from the anchor time
                            proj_dates_future = []
                            for k in range(actual_forward_periods): # Iterate up to the number of future points we actually have
                                future_time = projection_period_start_time + (k + 1) * interval_timedelta
                                proj_dates_future.append(future_time)
                            # --- ### END CORRECTED DATE CALCULATION ### ---

                            # Extend the plot lists with the calculated future points
                            plot_dates_this_match.extend(proj_dates_future)
                            plot_prices_this_match.extend(proj_prices_future)
                            proj_prices_future_for_ylim = proj_prices_future # Store for Y-lim
                        else:
                            logging.warning(f"M{i+1}: Historical end price zero. Skipping price projection.")
                    else:
                        # This case should be less likely now with adjusted end index, but good to log
                        logging.debug(f"M{i+1}: hist_forward data is empty (Indices: {hist_forward_start_idx} to {forward_end_idx}).")
                else:
                    logging.debug(f"M{i+1}: No forward data available (actual_forward_periods = {actual_forward_periods}). Only anchor point will be stored.")

                # Store the complete path (always includes anchor, may include future)
                if plot_dates_this_match:
                    all_projections_data.append({
                        'dates': plot_dates_this_match,
                        'prices': plot_prices_this_match,
                        'color': accent_colors[i % len(accent_colors)],
                        'alpha': 0.8,
                        'label': f'Projection #{i+1}',
                        'index': i
                    })
                else: logging.warning(f"M{i+1}: plot_dates_this_match ended up empty. Not storing.")

                # Collect ONLY future prices for Y-axis limit calculation
                if proj_prices_future_for_ylim:
                    all_projected_prices_for_ylim.extend(proj_prices_future_for_ylim)

            except IndexError as ie:
                 logging.error(f"Error processing match #{i+1} (IndexError): {ie}. Data might be too short.")
            except Exception as e:
                logging.error(f"Error processing match #{i+1}: {e}", exc_info=True)

        # Add the anchor price itself ONCE for Y-limit calculation
        all_projected_prices_for_ylim.append(current_final_price)

        # --- Calculate Aggregate Projection & Recommendations ---
        # (Aggregation logic remains the same)
        aggregate_dates = []
        aggregate_prices = []
        trade_direction = None
        entry_levels = []
        take_profit_levels = []
        target_projection_prices = [] # Prices used for recommendation logic
        aggregate_label = "Aggregate Projection"

        projections_for_calc = []
        if projection_method == 'top_match' and all_projections_data:
            projections_for_calc = [all_projections_data[0]]
            aggregate_label = "Top Match Projection"
            logging.info("Using 'top_match' projection for calculations (Match #1)")
        elif projection_method in ['median', 'avg'] and all_projections_data:
            # Ensure projection_top_n doesn't exceed the number of available projections
            num_available_projections = len(all_projections_data)
            actual_top_n = min(projection_top_n, num_available_projections)
            if actual_top_n < projection_top_n:
                 logging.warning(f"Requested top {projection_top_n} for aggregation, but only {num_available_projections} available. Using top {actual_top_n}.")
            elif actual_top_n == 0:
                 logging.warning("No projections available for aggregation.")

            if actual_top_n > 0:
                projections_for_calc = all_projections_data[:actual_top_n]
                aggregate_label = f"{projection_method.capitalize()} Projection (Top {len(projections_for_calc)})"
                logging.info(f"Using '{projection_method}' projection from top {len(projections_for_calc)} matches for calculations")
            else: # Handle case where no projections were successfully processed
                 projections_for_calc = []
        else:
            logging.warning("No valid projection data or unsupported projection method for calculations.")

        if projections_for_calc:
            max_len = 0
            for proj in projections_for_calc: max_len = max(max_len, len(proj.get('dates', [])))

            if max_len > 0:
                prices_at_step = [[] for _ in range(max_len)]
                dates_at_step = [[] for _ in range(max_len)]

                for proj in projections_for_calc:
                    proj_len = len(proj.get('dates', []))
                    for j in range(proj_len):
                        if j < max_len and j < len(proj.get('prices', [])):
                            prices_at_step[j].append(proj['prices'][j])
                            dates_at_step[j].append(proj['dates'][j])

                for j in range(max_len):
                    if prices_at_step[j]:
                        agg_price, agg_date = np.nan, None
                        valid_dates_step = [d for d in dates_at_step[j] if d is not None]
                        if not valid_dates_step: continue

                        if projection_method == 'top_match':
                            agg_price = prices_at_step[j][0]; agg_date = valid_dates_step[0]
                        elif projection_method == 'median':
                            agg_price = np.median(prices_at_step[j])
                            median_idx = np.argmin(np.abs(np.array(prices_at_step[j]) - agg_price))
                            agg_date = valid_dates_step[median_idx % len(valid_dates_step)]
                        elif projection_method == 'avg':
                            agg_price = np.mean(prices_at_step[j])
                            timestamps = [(d - projection_period_start_time).total_seconds() for d in valid_dates_step]
                            if timestamps: agg_date = projection_period_start_time + pd.Timedelta(seconds=np.mean(timestamps))
                            else: agg_date = valid_dates_step[0]

                        if not np.isnan(agg_price) and agg_date is not None:
                            aggregate_dates.append(agg_date); aggregate_prices.append(agg_price)

            if len(aggregate_prices) > 1:
                target_projection_prices = aggregate_prices
                logging.debug(f"Aggregate ({projection_method}) prices calc'd, len: {len(target_projection_prices)}")
            else: target_projection_prices = []; logging.warning(f"Aggregate proj ({projection_method}) too short/failed.")
        else: target_projection_prices = []; logging.warning("No data available for aggregate.")

        # --- Plot Projections (Bottom Panel) ---
        # (Plotting logic remains the same, handles single points)
        for proj_data in all_projections_data:
            if proj_data.get('dates') and proj_data.get('prices') and len(proj_data['dates']) == len(proj_data['prices']):
                line_alpha = proj_data['alpha']
                line_label = proj_data['label']
                marker = None
                linestyle = '-'
                if len(proj_data['dates']) == 1:
                    marker = 'o'
                    linestyle = ''
                    logging.debug(f"Plotting single anchor for Proj #{proj_data.get('index', 'N/A')+1}")

                # Premium styling for projections
                color = proj_data['color']  # This should already use accent_colors from data prep
                base_thickness = 5.0
                thickness = base_thickness / (golden_ratio ** proj_data['index'])
                if projection_method == 'top_match' and proj_data['index'] == 0:
                    thickness = base_thickness * golden_ratio / 1.618
                    line_label = f"{line_label} (Most Predictive)"  # Already in bot

                ax3.plot(proj_data['dates'], proj_data['prices'], linewidth=thickness, color=color,
                        linestyle=linestyle, marker=marker, alpha=line_alpha, label=line_label, zorder=10)
            else:
                logging.warning(f"Plot Skip: Proj #{proj_data.get('index', 'N/A')+1} missing/mismatched data.")

        if projection_method in ['median', 'avg'] and aggregate_dates and aggregate_prices:
            if len(aggregate_dates) == len(aggregate_prices):
                aggregate_alpha = 0.6
                aggregate_label = f"{aggregate_label} (Most Predictive)"  # Already in bot
                ax3.plot(aggregate_dates, aggregate_prices, linewidth=6, color='#ff6f00',  # Changed from 'black' to orange
                        linestyle='-', alpha=aggregate_alpha, label=aggregate_label, zorder=20)
            else:
                logging.error("Aggregate dates/prices mismatch. Cannot plot.")
        elif projection_method in ['median', 'avg']:
            logging.warning(f"Cannot plot aggregate line ({projection_method}) - data empty/failed.")

        ax3.axvline(x=projection_period_start_time, color='#d32f2f', linestyle='--', alpha=0.5, 
                   linewidth=2.5, label='Forecast Start', zorder=5)

        # --- Calculate Recommendations ---
        # (Recommendation logic remains the same)
        if current_final_price > 1e-9 and len(target_projection_prices) > 1:
            # Calculate min/max percentage changes from current price
            min_pct = min((p / current_final_price - 1) for p in target_projection_prices)
            max_pct = max((p / current_final_price - 1) for p in target_projection_prices)

            # Determine trade direction based on dominant movement
            if abs(min_pct) > abs(max_pct): trade_direction = "SHORT"
            else: trade_direction = "LONG"

            if trade_direction=="LONG":
                entry_end=current_final_price*(1+min(0,min_pct)); entry_levels=np.linspace(current_final_price,entry_end,num_entry_orders).tolist()
                avg_entry_reco=np.mean(entry_levels); tp_start=max(avg_entry_reco*1.005,current_final_price*1.001)
                tp_end=current_final_price*(1+max_pct); take_profit_levels=np.linspace(tp_start,tp_end,num_tp_orders).tolist() if tp_end>tp_start else [tp_start]*num_tp_orders
            elif trade_direction=="SHORT":
                entry_end=current_final_price*(1+max(0,max_pct)); entry_levels=np.linspace(current_final_price,entry_end,num_entry_orders).tolist()
                avg_entry_reco=np.mean(entry_levels); tp_start=min(avg_entry_reco*0.995,current_final_price*0.999)
                tp_end=current_final_price*(1+min_pct); take_profit_levels=np.linspace(tp_start,tp_end,num_tp_orders).tolist() if tp_end<tp_start else [tp_start]*num_tp_orders

            if trade_direction:
                logging.info(f"Calculated Recos: Dir={trade_direction}, Entries={entry_levels}, TPs={take_profit_levels}")
                # --- BOT DEBUG I/O: Log final recommendations ---
                if debug_io_flag:
                    logging.info("\n--- BOT DEBUG I/O: Final Recommendations ---")
                    reco_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
                    logging.info(f"Recommendations generated at: {reco_time}")
                    logging.info(f"Anchor Price at Forecast Start: {current_final_price:.4f}")
                    logging.info(f"Trade Direction: {trade_direction}")
                    entry_str = ", ".join([f"{p:.4f}" for p in entry_levels])
                    tp_str = ", ".join([f"{p:.4f}" for p in take_profit_levels])
                    logging.info(f"Entry Levels: [{entry_str}]")
                    logging.info(f"Take Profit Levels: [{tp_str}]")
                    logging.info("--- End BOT DEBUG I/O ---")
        else: logging.warning("Cannot calc recos: Anchor price zero or target proj too short.")


        # --- Final Plot Formatting ---
        # Y-Limits
        if all_projected_prices_for_ylim:
            min_price = min(all_projected_prices_for_ylim)
            max_price = max(all_projected_prices_for_ylim)
            price_range = max_price - min_price
            pad = price_range * 0.15
            if price_range > 0:
                ax3.set_ylim(min_price - pad, max_price + pad)
            else:  # Handle zero range
                ax3.set_ylim(min_price * 0.95 if min_price != 0 else -0.1, 
                            max_price * 1.05 if max_price != 0 else 0.1)

        # Grids
        ax3.grid(False)
        ax3.set_axisbelow(True)

        # Font Sizes
        base_fontsize = 12
        large_fontsize = int(base_fontsize * golden_ratio)
        medium_fontsize = int(base_fontsize * golden_ratio / 1.3)
        golden_padding = int(12 * golden_ratio)

        # Axis Labels
        ax3.set_xlabel('Forecast Time', fontsize=medium_fontsize, 
                      labelpad=golden_padding, color='#1a1a1a', fontweight='600', 
                      family='serif', style='normal')
        ax3.set_ylabel('Price Forecast ($)', fontsize=medium_fontsize, 
                      labelpad=golden_padding, color='#1a1a1a', fontweight='600', 
                      family='serif', style='normal')

        # In-Axis Titles
        title_fontsize = large_fontsize
        title_padding_factor = golden_ratio * 0.5
        title_y_position = 0.95
        title_style_base = dict(boxstyle=f"round,pad={title_padding_factor}", 
                              facecolor='#ffffff', alpha=0.98, 
                              linewidth=golden_ratio/2, linestyle='-')

        # For ax3 title
        ax3.text(0.7, title_y_position, f'Future Price Forecasts - {time_str} Forward',
                transform=ax3.transAxes, fontsize=title_fontsize, fontweight='700', ha='center', va='top',
                bbox=dict(**title_style_base, edgecolor='#c62828'), color='#b71c1c', family='serif')

        # Spines
        spine_config = {'linewidth': 3, 'alpha': 0.8}
        # For ax3
        for spine_name, spine in ax3.spines.items():
            if spine_name in ['top', 'right']: spine.set_visible(False)
            else: spine.set_color('#d32f2f'); spine.set(**spine_config)

        # Tick Parameters
        tick_params_config = {'axis': 'both', 'colors': '#424242', 'labelsize': 11, 'width': 2, 'length': 6}
        ax3.tick_params(**tick_params_config)

        # Legends
        # For ax3 legend
        handles3, labels3 = ax3.get_legend_handles_labels()
        if handles3:
            legend3 = ax3.legend(handles3, labels3, bbox_to_anchor=(0.06, 1), loc='upper left',
                               framealpha=0.99, fontsize=10, fancybox=True, shadow=True,
                               facecolor='#ffffff', edgecolor='#c62828', labelcolor='#2c2c2c',
                               title='Future Price Forecasts', title_fontsize=11,
                               borderpad=1.5, columnspacing=1.2, handlelength=2.5, handletextpad=1.0, frameon=True)
            legend3.get_title().set_color('#b71c1c')
            legend3.get_title().set_fontweight('700')
            legend3.get_title().set_family('serif')
            legend3.get_frame().set_linewidth(2.5)
            legend3.get_frame().set_boxstyle("round,pad=0.6")
            legend3.get_frame().set_alpha(0.99)

        # X-Axis Formatting for ax3
        # Collect all forecast dates for smart x-axis formatting for ax3
        ax3_forecast_dates = [current_final_date]  # Bot uses projection_period_start_time, but current_final_date is anchor for display
        if hasattr(current_data, 'open_time') and not current_data.open_time.empty:
            ax3_forecast_dates = [current_data.open_time.iloc[-1] + interval_timedelta]
        else:
            ax3_forecast_dates = [datetime.utcnow()]

        for proj_data_item in all_projections_data:
            if proj_data_item.get('dates'):
                ax3_forecast_dates.extend(proj_data_item['dates'])
        if aggregate_dates:
            ax3_forecast_dates.extend(aggregate_dates)
        ax3_valid_forecast_dates = sorted(list(set(d for d in ax3_forecast_dates if pd.notnull(d))))

        # Enhanced X-axis formatting for ax3
        if ax3_valid_forecast_dates and len(ax3_valid_forecast_dates) > 1:
            ax3_date_range = max(ax3_valid_forecast_dates) - min(ax3_valid_forecast_dates)
            if ax3_date_range.days > 7:
                ax3.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
                ax3.xaxis.set_minor_locator(mdates.HourLocator(interval=6))
                plt.setp(ax3.get_xticklabels(), rotation=60, ha='right', fontsize=8)
            elif ax3_date_range.days > 2:
                ax3.xaxis.set_major_locator(mdates.HourLocator(interval=12))
                ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
                plt.setp(ax3.get_xticklabels(), rotation=50, ha='right', fontsize=9)
            else:
                ax3.xaxis.set_major_locator(mdates.HourLocator(interval=6))
                ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
                plt.setp(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=9)
        else:
            ax3.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
            plt.setp(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=9)

        # --- STRATEGIC MARKERS ALIGNED WITH X-AXIS TICKS ---
        fig.canvas.draw()  # Only need to draw the main figure 'fig'

        ax3_tick_locs_num = ax3.get_xticks()

        # --- Plot Markers for ax3 (Projections) ---
        # Anchor date for projections (ensure this aligns with how projections start)
        anchor_date_for_proj_markers = projection_period_start_time

        for proj_data_item in all_projections_data:
            if proj_data_item.get('dates') and proj_data_item.get('prices'):
                plot_dates_ax3 = proj_data_item['dates']
                plot_prices_ax3 = proj_data_item['prices']
                if len(plot_dates_ax3) > 1:
                    color_ax3_markers = proj_data_item['color']
                    proj_index_ax3 = proj_data_item['index']
                    marker_style_ax3 = ['o', 's', '^', 'D', 'v', 'P', 'X', '*', 'h', 'p'][proj_index_ax3 % 10]
                    plot_markers_on_line(ax3, pd.to_datetime(pd.Series(plot_dates_ax3)), pd.Series(plot_prices_ax3),
                                       ax3_tick_locs_num, color_ax3_markers, marker_style_ax3, 6 + (proj_index_ax3*0.3))

        if projection_method in ['median', 'avg'] and aggregate_dates and aggregate_prices:
            if len(aggregate_dates) > 1:
                plot_markers_on_line(ax3, pd.to_datetime(pd.Series(aggregate_dates)), pd.Series(aggregate_prices),
                                   ax3_tick_locs_num, '#ff6f00', 'D', 7)

        # Final Layout
        fig.tight_layout()

        # Save Figure to a consistent path
        charts_dir = "charts"
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)

        safe_prediction_type = prediction_type.split('-')[0].lower()
        filename = f"{safe_prediction_type}_prediction_chart.png"
        filepath = os.path.join(charts_dir, filename)

        # --- THE FIX FOR THREAD-SAFE PLOTTING ---
        # Instead of calling the global plt.savefig, call savefig on the figure object itself.
        fig.savefig(filepath, facecolor=bg_color, edgecolor='none', bbox_inches='tight')
        logging.info(f"Plot saved to {filepath}")
        
        # --- THIS IS THE FIX FOR THE RACE CONDITION ---
        # 1. Flush the canvas to ensure all data is sent to the backend for writing.
        fig.canvas.flush_events()
        
        # 2. Introduce a small, robust delay to allow the OS to finish writing.
        #    A simple time.sleep() is often sufficient and much simpler than
        #    complex file lock checks. 0.5 seconds is usually more than enough.
        time.sleep(0.5) 
        # --- END OF FIX ---

        # Instead of calling the global plt.close, close the specific figure object.
        plt.close(fig)
        return filepath, trade_direction, entry_levels, take_profit_levels, all_projections_data

    except Exception as e:
        logging.error(f"Error creating plot: {e}",exc_info=True)
        # Ensure we close the specific figure on error too
        if fig is not None and plt.fignum_exists(fig.number):
            plt.close(fig)
        return None,None,[],[],[]

def analyze_recent_fractals(symbol, interval, lookback, historical_data_path,
                            analysis_config, prediction_type, debug_io_flag, **kwargs):
    """
    Main analysis function that fetches data and uses the dispatcher to find matches.
    """
    logging.info(f"--- Starting {prediction_type} Fractal Analysis for {symbol} ({interval}) ---")

    try:
        window_size = analysis_config.get('window_size')
        if not window_size:
            logging.error("window_size not found in analysis_config. Aborting.")
            return None
        
        fetch_periods = lookback + window_size
        
        # 1. Fetch Data
        recent_data = get_binance_data(symbol=symbol, interval=interval, lookback_periods=fetch_periods)
        if recent_data.empty or len(recent_data) < window_size:
            logging.error("Failed to fetch sufficient recent data. Aborting analysis.")
            return None

        historical_data = load_historical_data(historical_data_path)
        if historical_data.empty:
            logging.error("Failed to load historical data. Aborting analysis.")
            return None

        recent_data.reset_index(inplace=True); recent_data.rename(columns={'timestamp': 'open_time'}, inplace=True)
        historical_data.reset_index(inplace=True); historical_data.rename(columns={'timestamp': 'open_time'}, inplace=True)
        
        # 2. Find Matches using the dispatcher
        matches = find_best_fractal_matches(
            recent_data=recent_data,
            historical_data=historical_data,
            analysis_config=analysis_config, # Pass the entire config dict
            debug_io_flag=debug_io_flag
        )

        if matches.empty:
            logging.warning(f"No fractal matches found for {prediction_type}.")
            return None

        # --- The rest of the function remains the same ---
        matches['current_start_idx'] = len(recent_data) - window_size
        
        # 3. Generate chart and projections
        plot_filename, trade_direction, entry_levels, take_profit_levels, raw_projections = plot_multiple_matches(
            matches=matches,
            recent_data=recent_data,
            historical_data=historical_data,
            window_size=window_size,
            forward_periods=window_size,
            prediction_type=prediction_type,
            # Pass plotting-related params from the config
            projection_method=analysis_config.get('proj_method', 'median'),
            projection_top_n=analysis_config.get('proj_top_n', 5),
            feature_cols=analysis_config.get('feature_cols'),
            debug_io_flag=debug_io_flag
        )
        
        current_price = recent_data['close'].iloc[-1]
        
        # 4. Send notification if enabled
        send_notifications = kwargs.get('send_notifications', False)
        if send_notifications and plot_filename and trade_direction:
            discord_client = kwargs.get('discord_client')
            telegram_client = kwargs.get('telegram_client')
            discord_channel_id = kwargs.get('discord_channel_id')
            telegram_chat_id = kwargs.get('telegram_chat_id')
            # Generate caption for the notification
            caption = f"🤖 {prediction_type} Fractal Signal - {symbol}\n"
            caption += f"📊 Direction: {trade_direction}\n"
            caption += f"💰 Current Price: ${current_price:.4f}\n"
            if entry_levels:
                entry_str = ", ".join([f"${p:.4f}" for p in entry_levels[:3]])
                caption += f"🎯 Entry: {entry_str}\n"
            if take_profit_levels:
                tp_str = ", ".join([f"${p:.4f}" for p in take_profit_levels[:3]])
                caption += f"💎 Take Profit: {tp_str}\n"
            caption += f"⏰ Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
            try:
                send_notification(
                    discord_client=discord_client,
                    telegram_client=telegram_client,
                    target_discord_channel_id=discord_channel_id,
                    target_telegram_chat_id=telegram_chat_id,
                    image_path=plot_filename,
                    caption=caption
                )
                logging.info(f"✅ Notification sent for {prediction_type} signal")
            except Exception as e:
                logging.error(f"❌ Failed to send notification: {e}")
        elif send_notifications:
            logging.info(f"🔕 No notification sent: Missing chart ({plot_filename}) or trade direction ({trade_direction}).")
        else:
            logging.info(f"🔕 Notifications are disabled for this run (prediction_type: {prediction_type}).")

        # 5. Create Signal File
        signal_payload = None # Initialize
        if trade_direction and current_price is not None:
            # --- MODIFY THIS CALL ---
            signal_payload = _create_and_save_signal_file( # Capture the return value
                prediction_type=prediction_type,
                symbol=symbol,
                trade_direction=trade_direction,
                anchor_price=current_price,
                projections_data=raw_projections,  # Pass the correct raw projection data
                debug_io_flag=debug_io_flag
            )
        else:
            if debug_io_flag:
                logging.info("No signal file created: insufficient projection data or no trade direction determined.")

        logging.info(f"--- Completed {prediction_type} Fractal Analysis ---")
        # --- ADD THIS LINE ---
        return signal_payload # Return the result

    except KeyboardInterrupt:
        logging.info("Analysis interrupted by user.")
        raise
    except Exception as e:
        logging.error(f"Error in analyze_recent_fractals: {e}", exc_info=True)
    # --- ADD THIS LINE ---
    return None # Ensure it returns None on exception

def _create_and_save_signal_file(prediction_type, symbol, trade_direction, anchor_price, projections_data, debug_io_flag=False):
    """
    Creates the JSON signal file for the FractalTrader bot.
    FILENAME IS NOW PAIR-SPECIFIC.
    """
    if not trade_direction or not projections_data:
        logging.warning("Signal file not generated: No trade direction or projection data.")
        return

    # 1. Transform the plot data
    projected_paths_features = []
    for proj in projections_data:
        prices = proj.get('prices', [])
        if len(prices) > 1:
            anchor = prices[0]
            future_prices = np.array(prices[1:])
            if anchor > 1e-9:
                pct_changes = (future_prices / anchor) - 1
                projected_paths_features.append({
                    'min_pct': float(np.min(pct_changes)),
                    'max_pct': float(np.max(pct_changes)),
                    'final_pct': float(pct_changes[-1]),
                    'avg_pct': float(np.mean(pct_changes)),
                    'median_pct': float(np.median(pct_changes)),
                })

    if not projected_paths_features:
        logging.warning("Signal file not generated: Could not extract valid projection features.")
        return

    # 2. Construct the signal payload
    signal_payload = {
        'timestamp_utc': datetime.utcnow().isoformat(),
        'symbol': symbol,
        'trade_direction': trade_direction,
        'current_price_at_decision': anchor_price,
        'projected_paths_features': projected_paths_features
    }

    # 3. *** KEY CHANGE HERE: Define filename based on prediction type AND symbol ***
    filename_prefix = prediction_type.split('-')[0].lower()
    safe_symbol = symbol.lower().replace('usdt', '')
    signal_filename = f"{filename_prefix}_prediction_signal_{safe_symbol}.json"

    # 4. Save the file
    try:
        with open(signal_filename, 'w') as f:
            json.dump(signal_payload, f, indent=4)
        logging.info(f"✅ Successfully generated prediction signal file: {signal_filename}")
        if debug_io_flag:
            logging.info(f"\n--- BOT DEBUG I/O: Signal File Content ---\n{json.dumps(signal_payload, indent=2)}")
        
        # --- ADD THIS LINE ---
        return signal_payload # Return the created payload
        
    except Exception as e:
        logging.error(f"❌ Failed to write prediction signal file '{signal_filename}': {e}")
    
    # --- ADD THIS LINE ---
    return None # Return None on failure

# --- REMOVED DUPLICATE DISCORD CLIENT CLASS ---
# The DiscordClient is already imported from .discord_client

# --- FractalNotifier Class (Unchanged) ---
class FractalNotifier:
    def __init__(self, config: dict, logger: logging.Logger,
                 api_key=None, api_secret=None,
                 telegram_client: TelegramClient = None,
                 discord_client: DiscordClient = None):
        self.config = config
        self.logger = logger
        
        # --- Extract parameters directly from the config dictionary ---
        self.symbol = config['symbol']
        self.interval = config['interval']
        self.historical_data_path = config['historical_data_path']
        self.lookback = config['lookback']
        self.debug = config.get('debug', False)
        self.send_notifications_in_debug = config.get('send_notifications_in_debug', False)
        
        self.send_discord_notifications = config.get('send_discord_notifications', False)
        self.send_telegram_notifications = config.get('send_telegram_notifications', False)
        
        # No longer need individual parameter extraction - config dict has everything
        
        # --- MODIFIED: Use ConnectionManager instead of direct client/twm ---
        self.connection_manager = ConnectionManager(
            api_key=api_key,
            api_secret=api_secret,
            logging=self.logger, # Pass the new logger object
            symbol=self.symbol
        )
        
        # --- NOTIFICATION SETUP ---
        # Initialize notification clients and settings
        self.discord_client = discord_client # Assign directly
        self.telegram_client = telegram_client # Assign directly
        
        # --- Store the SINGLE Discord channel ID ---
        self.discord_channel_id = discord_client.chat_id if discord_client else None # Update based on new structure
        # --- Store Telegram credentials ---
        self.telegram_chat_id = telegram_client.chat_id if telegram_client else None # Update based on new structure

        # Create Discord client if Discord notifications are enabled
        if self.send_discord_notifications:
            # --- MODIFIED: Use passed arguments directly, NO os.getenv here ---
            if self.discord_client:
                self.logger.info("Discord notifications enabled. Using provided client instance.")
            else:
                self.logger.error("Discord notifications enabled but no DiscordClient instance provided.")
                self.send_discord_notifications = False
        
        # Create Telegram client if Telegram notifications are enabled
        if self.send_telegram_notifications:
            # --- MODIFIED: Use passed arguments directly, NO os.getenv here ---
            if self.telegram_client:
                self.logger.info("Telegram notifications enabled. Using provided client instance.")
                # Remove the internal import, assuming it's at the top of the module
                # from .telegram_client import TelegramClient
            else:
                self.logger.error("Telegram notifications enabled but no TelegramClient instance provided.")
                self.send_telegram_notifications = False
        
        if not self.send_discord_notifications and not self.send_telegram_notifications:
            self.logger.info("Both Discord and Telegram notifications are disabled.")
        else:
            enabled_services = []
            if self.send_discord_notifications: enabled_services.append("Discord")
            if self.send_telegram_notifications: enabled_services.append("Telegram")
            self.logger.info(f"Notification services enabled: {', '.join(enabled_services)}")
        
        # Timing - using tuples like legacy bot for exact same behavior
        self.last_daily_prediction_time = None
        self.last_weekly_prediction_time = None
        self.last_monthly_prediction_time = None
        self._initial_times_set = False  # Flag to ensure times are set before processing updates
        
        # Control flags
        self.is_running = False
        self.debug_next_update = self.debug  # Trigger analysis on first kline if debug is True
        self._stop_event = threading.Event()  # Use a thread-safe event for stopping

        # --- ADD FIRST-RUN FLAGS ---
        self.is_first_daily_run = True
        self.is_first_weekly_run = True
        self.is_first_monthly_run = True
        # --- END ADD FIRST-RUN FLAGS ---

        # Optional candle logging for connection debug
        self.log_1m_candles = config.get('log_1m_candles', False)

    def _get_current_utc_time(self):
        """Get current UTC time."""
        return datetime.utcnow()

    def _set_initial_times(self):
        """Sets the initial day/week timestamps based on current UTC time."""
        if self._initial_times_set:
            return  # Prevent running multiple times

        logging.info("--- Setting Initial Timestamps ---")
        now_utc = self._get_current_utc_time()
        self.last_daily_prediction_time = (now_utc.year, now_utc.month, now_utc.day)
        self.last_weekly_prediction_time = (now_utc.isocalendar()[0], now_utc.isocalendar()[1])
        self.last_monthly_prediction_time = (now_utc.year, now_utc.month)
        self._initial_times_set = True  # Mark as done
        logging.info(f"Initial time set. Day: {self.last_daily_prediction_time}, Week: {self.last_weekly_prediction_time}, Month: {self.last_monthly_prediction_time}")

    def handle_kline_update(self, msg):
        """Processes kline messages and triggers analyses based on UTC time."""
        # Using a new thread for each analysis run to not block the websocket
        threading.Thread(target=self._trigger_analysis, args=(msg,), daemon=True).start()

    def _trigger_analysis(self, msg):
        """Internal method to handle kline updates and trigger analysis."""
        try:
            # Ensure initial times are set before processing updates
            if not self._initial_times_set:
                self.logger.info("Waiting for initial times to be set before processing kline updates...")
                return  # Do not process kline updates until times are set

            # Check for stream errors in the kline data itself
            if msg.get('e') == 'error':  # This check is for the overall message wrapper
                self.logger.error(f"WebSocket error message: {msg.get('m')}")
                return  # ConnectionManager will handle the reconnection
            
            # Check for connection timeout or other connection issues
            if not isinstance(msg, dict) or 'k' not in msg:
                self.logger.info(f"Received malformed or non-kline message: {msg}")
                return

            # Ensure kline data is present
            kline_data = msg.get('k')
            if not kline_data:
                self.logger.info(f"No kline data ('k') in message: {msg}")
                return

            # Use the kline's close time (T) from Binance as the source of truth for current time
            event_time_ms = kline_data.get('T')
            if event_time_ms is None:
                self.logger.info(f"No kline close time ('T') in kline data: {kline_data}")
                return
            
            now_utc = datetime.utcfromtimestamp(event_time_ms / 1000)
            current_day_tuple = (now_utc.year, now_utc.month, now_utc.day)
            current_week_tuple = (now_utc.isocalendar()[0], now_utc.isocalendar()[1])
            current_month_tuple = (now_utc.year, now_utc.month)

            # Daily Trigger (New Day)
            # Check for debug_next_update first to ensure it runs immediately if set
            if self.debug_next_update:
                self.logger.info("*** Debug mode: Triggering immediate predictions on kline update ***")
                self.debug_next_update = False  # Reset the flag after triggering
                self._run_daily_analysis('Daily-Debug')
                return  # Exit after debug trigger

            if current_day_tuple != self.last_daily_prediction_time:
                self.logger.info(f"*** New UTC Day Detected (from Kline @ {now_utc}): {current_day_tuple} (Previous: {self.last_daily_prediction_time}) ***")
                self.last_daily_prediction_time = current_day_tuple
                self.logger.info("-> Triggering Daily Analysis...")
                self._run_daily_analysis('Daily')  # MOVED INSIDE THE IF BLOCK

            # Weekly analysis disabled

            # Monthly analysis disabled

            # ---- Optional 1-minute candle heartbeat ----
            if self.log_1m_candles and kline_data.get('x'):
                try:
                    o = float(kline_data.get('o'))
                    h = float(kline_data.get('h'))
                    l = float(kline_data.get('l'))
                    c = float(kline_data.get('c'))
                    self.logger.info(f"[SPOT] 1m Candle Closed | O:{o:.2f} H:{h:.2f} L:{l:.2f} C:{c:.2f}")
                except Exception as _:
                    pass

        except Exception as e:
            self.logger.error(f"Unhandled error in _trigger_analysis: {e}")

    def _run_daily_analysis(self, prediction_type):
        """Run daily fractal analysis, suppressing notification on the first run."""
        try:
            base_notification_flag = (self.send_discord_notifications or self.send_telegram_notifications)
            is_debug_suppressed = self.debug and not self.send_notifications_in_debug
            should_send_notifications = base_notification_flag and not is_debug_suppressed and not self.is_first_daily_run
            
            if self.is_first_daily_run:
                self.logger.info(f"🔕 First daily run for {self.symbol} since startup. Analysis will run, but notifications are suppressed.")
                self.is_first_daily_run = False

            # The 'daily' dictionary from the main config already has everything we need.
            daily_analysis_config = self.config.get('daily', {})

            signal_payload = analyze_recent_fractals(
                symbol=self.symbol,
                interval=self.interval,
                lookback=self.lookback,
                historical_data_path=self.historical_data_path,
                analysis_config=daily_analysis_config, # Pass the whole 'daily' dict
                prediction_type=prediction_type,
                debug_io_flag=self.debug,
                send_notifications=should_send_notifications,
                discord_client=self.discord_client,
                discord_channel_id=self.discord_channel_id,
                telegram_client=self.telegram_client,
                telegram_chat_id=self.telegram_chat_id
            )

        except Exception as e:
            self.logger.error(f"Error in daily analysis: {e}", exc_info=True)

    # Weekly analysis method disabled

    # Monthly analysis method disabled

    # --- REMOVED: The old _start_twm_session and _stop_twm methods are no longer needed ---
    # def _start_twm_session(self): ...
    # def _stop_twm(self): ...

    def start(self):
        """Start the notifier using ConnectionManager."""
        if self.is_running:
            logging.warning("Notifier is already running")
            return
        
        self.is_running = True
        self.logger.info(f"Starting FractalNotifier for {self.symbol}")
        
        # --- MODIFIED: Start using ConnectionManager ---
        self.connection_manager.is_running = True
        
        if self.discord_client:
            self.discord_client.start()
        
        self._set_initial_times()
        
        # Start the kline websocket via the manager
        self.connection_manager.start_kline_websocket(
            symbol=self.symbol,
            interval=self.interval,
            callback=self.handle_kline_update
        )
        
        # Main loop - check health and wait
        try:
            while self.is_running and not self._stop_event.is_set():
                # --- ADDED: Regular health check ---
                self.connection_manager.check_connection_health()
                time.sleep(10) # Check health every 10 seconds
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received in notifier")
        finally:
            self.stop()

    def stop(self):
        """Stop the notifier and its ConnectionManager."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping FractalNotifier...")
        self.is_running = False
        self._stop_event.set()  # Signal loops to stop
        
        # --- MODIFIED: Stop the ConnectionManager ---
        self.connection_manager.stop()
        
        if self.discord_client:
            self.discord_client.stop()
        
        self.logger.info("FractalNotifier stopped")

# --- NEW: The Main FractalBot Class ---
class FractalBot:
    def __init__(self, config: dict, logger: logging.Logger,
                 api_key: str = None, api_secret: str = None,
                 telegram_client: TelegramClient = None,
                 discord_client: DiscordClient = None):
        self.config = config
        self.logger = logger
        self.symbol = config.get('symbol', 'BTCUSDT')
        
        # --- Fail-fast: Validate historical CSV exists at startup ---
        historical_data_path = config.get('historical_data_path')
        if not historical_data_path:
            self.logger.critical("CRITICAL: No 'historical_data_path' specified in config. Cannot proceed.")
            sys.exit(1)
        
        # Simple approach: if relative path, assume it's in the data/ directory
        if not os.path.isabs(historical_data_path):
            # Get project root (two levels up from src/)
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            data_dir = os.path.join(project_root, 'data')
            historical_data_path = os.path.join(data_dir, historical_data_path)
            
            # Update the config with the resolved path
            config['historical_data_path'] = historical_data_path
        
        # Check if the file exists
        if not os.path.exists(historical_data_path):
            self.logger.critical(
                f"CRITICAL: Historical CSV not found at '{historical_data_path}'.\n"
                "Ensure the file exists in the data/ directory before starting the bot."
            )
            sys.exit(1)
        
        self.logger.info(f"✅ Historical CSV validated: {historical_data_path}")
        
        self.client = Client(api_key, api_secret) # Binance client for historical data, not for WebSocket
        self.connection_manager = ConnectionManager(
            api_key=api_key,
            api_secret=api_secret,
            logging=self.logger,
            symbol=self.symbol
        ) # Pass standard logger
        self.notifier = FractalNotifier(
            config=config,
            logger=self.logger, # Pass the standard logger to notifier as well
            telegram_client=telegram_client,
            discord_client=discord_client,
            api_key=api_key,
            api_secret=api_secret
        )
        self.stop_event = threading.Event()
        self.logger.info("FractalBot initialized.")

    def run(self):
        """
        Starts the FractalBot by launching the continuous notifier loop.
        This single execution path correctly handles both live and debug modes.
        """
        try:
            logging.info(f"Starting FractalBot main loop for {self.symbol}...")
            # Start the notifier in a background thread; debug vs live behavior is internal
            self.notifier_thread = threading.Thread(target=self.notifier.start, daemon=True)
            self.notifier_thread.start()

            # Keep main thread alive while notifier runs
            while True:
                if not self.notifier_thread.is_alive():
                    logging.error("Notifier thread has unexpectedly died. Shutting down.")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        finally:
            logging.info("Main loop finished.")
    
    def stop(self):
        """Stops the FractalBot notifier gracefully."""
        # Check if already stopped to prevent redundant calls
        if self.notifier and self.notifier.is_running:
            logging.info(f"Stopping FractalBot for {self.symbol}...")
            self.notifier.stop()
            if hasattr(self, 'notifier_thread') and self.notifier_thread.is_alive():
                self.notifier_thread.join(timeout=10)
            logging.info(f"FractalBot for {self.symbol} has been stopped.")

# NOTE: The 'if __name__ == "__main__"' block from the old file is DELIBERATELY REMOVED.
# This file is now a library module, not a directly runnable script. 

==================================================
