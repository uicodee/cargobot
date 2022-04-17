import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClient


async def create_spreadsheet(client: AsyncioGspreadClient, spreadsheet_name):
    spreadsheet = await client.create(spreadsheet_name)
    spreadsheet = await client.open_by_key(spreadsheet.id)
    return spreadsheet


async def add_worksheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet, worksheet_name: str):

    worksheet = await async_spreadsheet.add_worksheet(worksheet_name, 1000, 100)
    worksheet = await async_spreadsheet.worksheet(worksheet_name)
    return worksheet


async def share_spreadsheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet, email: str, role: str = 'writer'):
    await async_spreadsheet.share(email, perm_type='user', role=role)
    return True