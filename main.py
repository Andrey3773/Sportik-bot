import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import (base_handlers as base,
                      insert_handlers as insert,
                      rest_handlers as rest,
                      output_handlers as output)
from config.config_env import load_config


async def main():
    config = load_config('.env')
    storage = MemoryStorage()
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)


    routers = [base.router, insert.router, rest.router, output.router]

    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


asyncio.run(main())
