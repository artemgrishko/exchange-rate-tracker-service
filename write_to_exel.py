import asyncio
import xlsxwriter
import aiosqlite


async def get_exchange_rate_from_db():
    async with aiosqlite.connect('exchange_rates.db') as conn:
        async with conn.execute(
                "SELECT id, datetime, exchange_rate FROM exchange_rates"
        ) as cursor:
            exchange_rate_data = await cursor.fetchall()

    return exchange_rate_data


async def write_to_excel(data):
    workbook = xlsxwriter.Workbook('exchange_rate.xlsx')
    worksheet = workbook.add_worksheet()

    yellow_columns = ['datetime', 'exchange_rate']
    yellow_format = workbook.add_format({'bg_color': 'yellow'})

    column_names = ['', 'datetime', 'exchange_rate']
    for i, column_name in enumerate(column_names):
        if column_name in yellow_columns:
            worksheet.write(0, i, column_name, yellow_format)
        else:
            worksheet.write(0, i, column_name)

    for row, (id, date, rate) in enumerate(data, start=1):
        worksheet.write(row, 0, id)

        worksheet.write_string(row, 1, str(date))
        worksheet.write_string(row, 2, str(rate))

    for i, column_name in enumerate(column_names):
        max_len = max([len(str(row[i])) for row in data + [column_names]])
        worksheet.set_column(i, i, max_len)

    workbook.close()


async def get_file():
    exchange_rate_data = await get_exchange_rate_from_db()
    await write_to_excel(exchange_rate_data)
    return 'exchange_rate.xlsx'


async def main():
    await get_file()


asyncio.run(main())
