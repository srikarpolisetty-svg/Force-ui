import time
import yfinance as yf
import pandas as pd
import ta
import os
import PublicAPI
from dotenv import load_dotenv

load_dotenv()

# ==============================
# PUBLIC API AUTH
# ==============================
client = PublicClient(
    api_key=os.getenv("PUBLIC_API_KEY"),
    api_secret=os.getenv("PUBLIC_API_SECRET"),
)

ACCOUNT_ID = os.getenv("PUBLIC_ACCOUNT_ID")
TICKER = "SPY"
CHECK_INTERVAL = 60


def get_current_position():
    """Return how many shares of SPY you currently own."""
    positions = client.get_positions(account_id=ACCOUNT_ID)

    for p in positions:
        if p["symbol"] == TICKER:
            return float(p["quantity"])
    return 0.0


def place_order(side):
    """Executes a real market order using Public API."""
    qty = 1  # <-- change this if you want more shares

    print(f"📤 EXECUTING REAL ORDER: {side.upper()} {qty} SHARE")

    resp = client.order_market(
        account_id=ACCOUNT_ID,
        symbol=TICKER,
        side=side,
        quantity=qty
    )

    print("✅ Order response:", resp)
    print("──────────────────────────────")


# ==============================
# LOOP FOREVER
# ==============================
while True:

    print("\n🔄 Checking SPY…")

    raw = yf.download(TICKER, period="1mo", interval="1d")

    data = pd.DataFrame()
    data["Close"] = raw["Close"].astype(float).squeeze()

    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"], window=14).rsi()
# extracting latest values for decision making
    price_now = data["Close"].iloc[-1]
    price_prev = data["Close"].iloc[-2]

    ma20_now = data["MA20"].iloc[-1]
    ma20_prev = data["MA20"].iloc[-2]

    ma50_now = data["MA50"].iloc[-1]
    ma50_3d_ago = data["MA50"].iloc[-3]

    rsi_now = data["RSI"].iloc[-1]
    rsi_prev = data["RSI"].iloc[-2]
# decision conditions
    cross_above_ma20 = (price_prev < ma20_prev) and (price_now > ma20_now)
    rsi_cross = (rsi_prev < 45) and (rsi_now > 50)
    price_above_ma50 = price_now > ma50_now
    ma50_uptrend = ma50_now > ma50_3d_ago

    position_qty = get_current_position()

    print(f"💹 Price: {price_now:.2f} | RSI: {rsi_now:.1f} | Position: {position_qty}")

    # =========================================
    # BUY CONDITION
    # =========================================
    if position_qty == 0:
        if (cross_above_ma20 or rsi_cross) and ma50_uptrend and price_above_ma50:
            print("🚀 BUY SIGNAL — executing market order...")
            place_order("buy")

        else:
            print("😐 HOLD")

    # =========================================
    # SELL CONDITION
    # =========================================
    else:  # position_qty > 0
        if not price_above_ma50:
            print("🔻 SELL SIGNAL — executing market order...")
            place_order("sell")

        else:
            print("😐 HOLD (still in trade)")

    print(f"⏳ waiting {CHECK_INTERVAL} sec...")
    time.sleep(CHECK_INTERVAL)
