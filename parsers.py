from configparser import ConfigParser
import lxml
import aiohttp
from bs4 import BeautifulSoup


class Parser:
    buffer = ConfigParser()

    def __init__(self):
        self.buffer.read("buffer.ini")


# TODO --------------------TEMPLATE--------------------
class StopGameRU(Parser):
    async def parse(self, user_agent: str) -> (str, str):
        async with aiohttp.ClientSession(headers={"User-Agent": user_agent}) as session:
            async with session.get('https://stopgame.ru/news') as resp:
                q = await resp.read()
        r = BeautifulSoup(q.decode('utf-8'), 'lxml')
        item = r.find_all("div", {"class": "article-summary"})[0]
        itemID = item["data-key"]
        name = item.a.img["alt"]
        link = "https://stopgame.ru" + item.a["href"]
        if not self.buffer.has_option("LastNews", self.__class__.__name__):
            self.buffer.set("LastNews", self.__class__.__name__, "-")
            with open("buffer.ini", 'w') as file:
                self.buffer.write(file)
        if itemID != self.buffer["LastNews"][self.__class__.__name__]:
            self.buffer["LastNews"][self.__class__.__name__] = itemID
            with open("buffer.ini", 'w') as file:
                self.buffer.write(file)
            return name, link
        else:
            return "", ""
