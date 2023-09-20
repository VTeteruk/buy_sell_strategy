import logging
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

logging.basicConfig(level=logging.INFO)


def get_data() -> pd.DataFrame:
    exchange = ccxt.binance()

    symbol = "BTC/USDT"
    timeframe = "1m"

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=60)

    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    df.to_csv("historical_data.csv", index=False)

    return df


def display_graph(df: pd.DataFrame, bought_points, sold_points) -> None:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    start_price = df["close"].iloc[0]

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df["close"], color="black", label="Price")
    plt.hlines(
        start_price,
        xmin=df.index[0],
        xmax=df.index[-1],
        colors="red",
        linestyles="dashed",
        label="Initial balance",
    )

    if bought_points:
        time, bought_prices = zip(*bought_points)
        plt.scatter(time, bought_prices, marker="v", color="red", label="Buy", s=100)

    if sold_points:
        time, sold_prices = zip(*sold_points)
        plt.scatter(time, sold_prices, marker="^", color="green", label="Sell", s=100)

    plt.title("BTC/USDT")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)

    date_format = DateFormatter("%H:%M:%S")
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)

    plt.show()


def main(
    df: pd.DataFrame,
    balance: int = 100_000_000,
    division_coefficient: int = 100,
) -> tuple[float | int, list, list]:

    initial_balance = balance
    bitcoins = 0

    successful_trades = 0
    total_trades = 0

    buying_steps = [0.001, 0.002, 0.001, 0.001]
    selling_steps = [0.004, 0.002, 0.003, 0.002]

    step_index = 0
    bought_bitcoins_points = []
    previous_price = df["close"][0]

    bought_points = []
    sold_points = []

    for _, row in df.iterrows():
        price = row["close"]
        time = row["timestamp"]
        if price <= previous_price * (
            1 - buying_steps[step_index] / division_coefficient
        ):
            if balance <= 0:
                if bitcoins:
                    logging.info(f"We have no money to buy BTC, but have {bitcoins} BTC")
                else:
                    logging.info("We have no money")
                continue

            amount_to_buy = balance / len(buying_steps)
            balance -= amount_to_buy
            bitcoins_to_buy = amount_to_buy / price
            bitcoins += bitcoins_to_buy
            bought_bitcoins_points.append((price, bitcoins_to_buy, step_index))

            step_index = (step_index + 1) % len(buying_steps)
            total_trades += 1
            bought_points.append((time, price))

            logging.info(f"Bought {bitcoins_to_buy} BTC at {price}")
        elif price > previous_price:
            step_index = 0

            for index, (
                price_BTC_was_bought,
                amount_of_bitcoins,
                step_index,
            ) in enumerate(bought_bitcoins_points):
                if price_BTC_was_bought <= price * (
                    1 - selling_steps[step_index] / division_coefficient
                ):
                    profit = amount_of_bitcoins * price

                    if profit - price_BTC_was_bought * amount_of_bitcoins > 0:
                        logging.info(
                            f"Sold at {price} "
                            f"(+{profit - price_BTC_was_bought * amount_of_bitcoins})"
                        )
                        successful_trades += 1
                    else:
                        logging.info(
                            f"Sold at {price} "
                            f"({profit - price_BTC_was_bought * amount_of_bitcoins})"
                        )

                    sold_points.append((time, price))

                    balance += profit
                    bitcoins -= amount_of_bitcoins
                    bought_bitcoins_points.pop(index)

        previous_price = price

    balance += bitcoins * df["close"].iloc[-1]

    total_profit = balance - initial_balance
    print(f"Successful Trades: {successful_trades}")
    print(f"Total Trades: {total_trades}")
    print(f"Final Balance: {balance}")
    print(f"Total profit: {total_profit}")

    return total_profit, bought_points, sold_points


if __name__ == "__main__":
    data = get_data()
    _, buy_points, sell_points = main(data)
    display_graph(data, bought_points=buy_points, sold_points=sell_points)
