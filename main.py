from src.interface.user_interface import run
from src.utils.currency_loader import fetch_and_save_currency_rates

if __name__ == "__main__":
    fetch_and_save_currency_rates()
    run()
