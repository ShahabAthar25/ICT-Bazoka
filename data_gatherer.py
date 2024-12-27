import toml, os
import yfinance as yf
from utils import setup_logger, time_period_to_dates

logger = setup_logger(__name__, log_file="data_gatherer.log")

logger.info("Reading Config...")

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config = toml.load(f"{CURRENT_DIR}/config.toml")["Data"]

storage_path = f"{CURRENT_DIR}/{config['storage']}"
symbols = config["symbols"]

logger.info("Converting time period to starting and ending dates.")
starting_date, ending_date  = time_period_to_dates(time_period=config["period"])


if not os.path.isdir(storage_path):
    logger.warning("Data folder not found. Creating one...")
    os.mkdir(storage_path)
    
for symbol in symbols:
    symbol_storage_path = f"{storage_path}/{symbol}"
    if not os.path.isdir(symbol_storage_path):
        logger.warning("Symbol folder not found in Data folder. Creating one...")
        os.mkdir(symbol_storage_path)

    for interval in config["intervals"]:
        logger.info(f"Downloading data (Symbol: {symbol}, Interval: {interval})")
        data = yf.download(tickers=symbol, start=starting_date, end=ending_date, interval=interval)
        logger.info(f"Writing data...")
        data.to_csv(f"{symbol_storage_path}/{interval}.csv")
        