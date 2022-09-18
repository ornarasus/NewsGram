import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from parsers import *

# TODO --------------------SETTINGS--------------------
Token = ""
ChannelID = "@ChannelLink"
Parsers = [StopGameRU()]
Timeout = 3600  # seconds
UserAgent = "Opera/8.75 (X11; Linux x86_64; sl-SI) Presto/2.12.306 Version/11.00"

bot = Bot(token=Token, parse_mode="HTML")
dp = Dispatcher(bot)


async def main():
    while True:
        try:
            for news in Parsers:
                title, link = await news.parse(UserAgent)
                if title != "":
                    await bot.send_message(ChannelID, f"{title}\n{link}")
        except RuntimeWarning:
            executor.start_polling(dp, skip_updates=True)
        finally:
            await asyncio.sleep(Timeout)

try:
    if __name__ == '__main__':
        asyncio.run(main())
except KeyboardInterrupt:
    pass
