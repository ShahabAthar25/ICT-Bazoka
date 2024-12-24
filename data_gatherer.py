import toml, os
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

config = toml.load("config.toml")

duration = config["data_harvesting"]["starting_date"]
symbol = config["data_harvesting"]["symbol"]
timeframe = config["data_harvesting"]["timeframe"]

data_location_folder = config["data_harvesting"]["location"]
data_location_symbol = os.path.join(os.path.dirname(os.path.realpath(__file__)), data_location_folder, symbol)

if not os.path.isdir(data_location_symbol):
    os.mkdir(data_location_symbol)

data_location = os.path.join(data_location_symbol, timeframe)

if not os.path.isdir(data_location):
    os.mkdir(data_location)

current_date = datetime.now()

starting_date = current_date - relativedelta(months=duration)
time_interval = current_date

while time_interval > starting_date:
    _starting_date = time_interval - relativedelta(months=1)
    csv_location = os.path.join(data_location, f"{_starting_date.strftime('%Y-%m-%d')}.csv")

    if os.path.exists(csv_location):
        time_interval = _starting_date
        print(f"Already have data for month {_starting_date} (Symbol: {symbol} Timeframe: {timeframe})")
        
        continue

    df = yf.download(
        symbol,
        interval=timeframe,
        start=str(_starting_date.strftime("%Y-%m-%d")),
        end=str(time_interval.strftime("%Y-%m-%d"))
    )

    if df.shape[0] > 100 and df.shape[1] > 3:
        df.to_csv(csv_location, index=False)
        print(f"Stored data for month {_starting_date.strftime("%Y-%m-%d")} (Symbol: {symbol} Timeframe: {timeframe})")
    else:
        print(f"An error occured while storing data for month {_starting_date.strftime("%Y-%m-%d")} (Symbol: {symbol} Timeframe: {timeframe})")
        print(f"Error: {Exception}")
        
    
    
    time_interval = _starting_date