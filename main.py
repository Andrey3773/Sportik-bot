import asyncio
import asyncpg

from asyncpg.pool import Pool
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

    db_pool: Pool = await asyncpg.create_pool( # noqa
        user=config.db.db_user,
        password=config.db.db_password,
        database=config.db.db_name,
        host=config.db.db_host,
        min_size=1,
        max_size=10,
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    dp["db_pool"] = db_pool


    routers = [base.router, insert.router, rest.router, output.router]

    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await db_pool.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
