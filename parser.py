import asyncio
from time import sleep

import aiohttp
import aiosqlite
from bs4 import BeautifulSoup
from datetime import datetime

import schedule

URL = "https://www.google.com/finance/quote/USD-UAH"


async def get_rate():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            rate = soup.select_one(
                "div:nth-of-type(2) > div > c-wiz "
                "> div > div > div > div > div > div > div > span > div"
            ).text
            return rate


async def save_rate_to_db_async(rate: str):
    async with aiosqlite.connect('exchange_rates.db') as conn:
        await conn.execute(
            '''CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                exchange_rate TEXT)'''
        )

        await conn.execute(
            '''INSERT INTO exchange_rates (datetime, exchange_rate) VALUES (?, ?)''',
            (datetime.now(), rate)
        )

        await conn.commit()


async def scrape_all():
    rate = await get_rate()
    print(f"Current rate: {rate}")
    await save_rate_to_db_async(rate)


def job():
    asyncio.run(scrape_all())


if __name__ == "__main__":
    schedule.every().minute.do(job)
    while True:
        schedule.run_pending()
        sleep(1)
