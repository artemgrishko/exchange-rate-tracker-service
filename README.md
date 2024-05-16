# Exchange Rate Tracker Service

## Features
- Web Scraping:  fetches the exchange rate from the specified URL using Requests, then parses the HTML response with BeautifulSoup to extract the rate value. It then saves the rate along with the current timestamp to a SQLite database. The script runs in an infinite loop, scraping the rate and saving it to the database every hour.
- Telegram Bot: bot provides a convenient command to upload an XLSX file containing current daily exchange rate statistics. Users can utilize the command /get_exchange_rate to receive the latest exchange rate information in an easily accessible format.


## Installing using GitHub

```shell
git clone https://github.com/artemgrishko/exchange-rate-tracker-service.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set BOT_TOKEN=<Your Telegram Bot Token>
```

**Run the Web Scraping Script:**
```shell
python parser.py
```

**For running the Telegram Bot you need create new Terminal and execute command:**
```shell
python bot.py
```

