import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from kleinanzeigen import parse, KleinanzeigenAPI

from dotenv import load_dotenv

load_dotenv()

cache = list()

requests = [
    {
        "keywords": ["iphone", "defekt"],
        "max_price":100,
        "min_price":0,
        "location_id":6411,
        "category_id":173,
    },
    {
        "keywords": ["fernseher"],
        "max_price":80,
        "min_price":0,
        "location_id":6411,
        "category_id":175,
    }
]

USER_ID = os.getenv("USER_ID")
TOKEN = os.getenv("TOKEN")

async def observer(bot: Bot):
    while True:
        for request in requests: 
            offers = await parse(**request)
            for offer in offers:
                id = str(USER_ID) + offer["id"]
                if id in cache:
                    break
                if offer["pro"] or offer["top"]:
                    continue
                response = (
                    "<b>Ich finde neue Anzeige!</b> {created_at}\n\n"
                    "<b>Titel</b>: {title}\n"
                    "<b>Preise</b>: {price} Euro <s>{discount}</s>\n"
                    "<b>Ort</b>: {location}\n"
                    "<b>Description</b>: {description}\n\n"
                    "<b>Verstand möglich</b>: {delivery}\n"
                    "<b>VB</b>: {is_vb}\n\n"
                    "<b><a href=\"{url}\">Link</a></b>"
                ).format(
                    title=offer.get("title"),
                    price=offer["price"], 
                    discount=offer["discount"] if offer["discount"] else "",
                    url=KleinanzeigenAPI.ENDPOINT + offer["url"],
                    description=offer["description"],
                    delivery="JA" if offer["delivery"] else "Nein",
                    is_vb="JA" if offer["is_VB"] else "Nein",
                    location=offer["location"],
                    created_at=offer["created_at"]
                )
                await bot.send_photo(chat_id=USER_ID, caption=response, photo=offer["image"].replace("_2", "_59"))   
                cache.append(id)
                break         
            await asyncio.sleep(1)
        await asyncio.sleep(10)

async def start():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    asyncio.ensure_future(observer(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())