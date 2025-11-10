from publicdotcom.api import PublicAPI
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

api = PublicAPI(
    api_key=os.getenv("PUBLIC_API_KEY"),
    api_secret=os.getenv("PUBLIC_API_SECRET"),
)

def buy_spy(amount_dollars):
    print(f"🚀 Sending BUY order → ${amount_dollars} of SPY")

    order = api.submit_order(
        symbol="SPY",
        side="buy",
        type="market",
        fractional=amount_dollars,  # <-- INVEST $ AMOUNT
        time_in_force="day",
    )

    print(order)


def sell_spy(amount_dollars):
    print(f"🔻 Sending SELL order → ${amount_dollars} of SPY")

    order = api.submit_order(
        symbol="SPY",
        side="sell",
        type="market",
        fractional=amount_dollars,
        time_in_force="day",
    )

    print(order)


if __name__ == "__main__":
    # 👇 Example (uncomment to test)
    # buy_spy(50)
    # sell_spy(50)
    pass
