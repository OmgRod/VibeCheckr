import os
import asyncio
from dotenv import load_dotenv
from src.client import MyClient
from src.dashboard import start_dashboard

load_dotenv()

async def main():
    client = MyClient()
    start_dashboard()
    await client.start(os.getenv("BOT_TOKEN"))

asyncio.run(main())
