import json
import os
from datetime import datetime

EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "EGP": 30.90,
    "GBP": 0.79,
    "JPY": 150.0
}

HISTORY_FILE = "conversion_history.json"


def convert_currency(amount, from_currency, to_currency):
    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError
    except ValueError:
        return "Error: Please enter a valid positive number."

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return f"Error: Supported currencies: {', '.join(EXCHANGE_RATES.keys())}"

    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    converted_amount = round(amount_in_usd * EXCHANGE_RATES[to_currency], 2)

    log_conversion(amount, from_currency, converted_amount, to_currency)
    return converted_amount


def log_conversion(original_amount, from_curr, converted_amount, to_curr):
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_currency": from_curr,
        "target_currency": to_curr,
        "original_amount": original_amount,
        "converted_amount": converted_amount
    }

    history = []

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
        except json.JSONDecodeError:
            history = []

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def run_cli():
    print("=== Currency Converter CLI ===")
    print("Type 'exit' anytime to quit.\n")

    while True:
        amount = input("Enter amount: ")
        if amount.lower() == "exit":
            break

        from_curr = input("From currency: ")
        if from_curr.lower() == "exit":
            break

        to_curr = input("To currency: ")
        if to_curr.lower() == "exit":
            break

        result = convert_currency(amount, from_curr, to_curr)
        print("Result:", result)
        print("-" * 40)


if __name__ == "__main__":
    run_cli()
