import random
import yfinance as yf
from datetime import datetime, timezone, timedelta
import json
import os

TICKERS = [
    # Core AI Compute
    "NVDA", "AMD", "AVGO", "MRVL", "TSM",
    
    # AI Networking & Interconnect
    "CRDO", "ALAB", "CIEN", "ANET",
    
    # Photonics / Optical
    "COHR", "LITE", "AAOI", "GLW", "FN",
    
    # Memory
    "MU", "STX", "RMBS",
    
    # Power & Energy for Data Centers
    "MPWR", "VRT", "AMSC",
    
    # Manufacturing / Testing / Equipment
    "CLS", "AEHR", "AMAT", "LRCX", "KLAC",
    
    # Other AI Infrastructure
    "NBIS", "ARM", "SMTC", "MXL"
]

DATA_FILE = "data/purchases.json"

def get_random_stock_and_fractional_shares(payment_amount: float = 25.0):
    ticker_symbol = random.choice(TICKERS)
    ticker = yf.Ticker(ticker_symbol)

    try:
        price = ticker.fast_info.get("lastPrice") or ticker.info.get("regularMarketPrice")
        if not price or price <= 0:
            price = 100.0
    except Exception:
        price = 100.0

    shares = round(payment_amount / price, 6)

    return {
        "ticker": ticker_symbol,
        "shares": shares,
        "price": round(price, 2),
        "total": payment_amount,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def create_timeline(purchase: dict) -> list:
    base_time = datetime.fromisoformat(purchase["timestamp"])

    market_makers = [
        "Citadel Securities",
        "Virtu Financial",
        "Jane Street",
        "Two Sigma Securities",
        "Jump Trading",
        "GTS Securities",
        "IMC",
        "Optiver"
    ]

    exchanges = [
        "Nasdaq",
        "NYSE",
        "Cboe EDGX",
        "Cboe BZX",
        "IEX",
        "MEMX"
    ]

    selected_mm = random.choice(market_makers)
    selected_exchange = random.choice(exchanges)

    settlement_time = base_time + timedelta(days=1)

    events = [
        {
            "time": base_time.isoformat(),
            "event": "Payment confirmed via Stripe (test mode)"
        },
        {
            "time": (base_time + timedelta(seconds=2)).isoformat(),
            "event": f"Order routed to {selected_exchange}"
        },
        {
            "time": (base_time + timedelta(seconds=4)).isoformat(),
            "event": f"Market maker {selected_mm} filled {purchase['shares']} shares of {purchase['ticker']} at ${purchase['price']}"
        },
        {
            "time": (base_time + timedelta(seconds=7)).isoformat(),
            "event": "Trade submitted to NSCC (DTCC) for clearing & netting"
        },
        {
            "time": (base_time + timedelta(seconds=10)).isoformat(),
            "event": f"Trade accepted by DTCC • Settlement scheduled for T+1 ({settlement_time.strftime('%Y-%m-%d')})"
        },
        {
            "time": settlement_time.isoformat(),
            "event": "T+1 Settlement complete • Book-entry transfer finished at DTC • Shares now Settled in your account"
        }
    ]
    return events

def save_purchase(purchase: dict, timeline: list):
    os.makedirs("data", exist_ok=True)

    record = {
        **purchase,
        "timeline": timeline,
        "status": "Settled"
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_purchases():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)
