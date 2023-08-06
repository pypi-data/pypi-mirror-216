""" Сборка бота """

import asyncio
from loguru import logger

from src.core.db import database_init

from curcheck import Dispatcher

from src.router import router


dp = Dispatcher()


async def start_bot():
    # include routers
    logger.info("Include base_router")
    dp.include_router(
        router=router
    )

    logger.info("Start polling")
    await dp.start()


async def start_app():
    logger.info("Main start app")

    await database_init()

    await asyncio.gather(
        start_bot() # Можно добавить подключение сайта, если надо
    )


if __name__ == "__main__":
    logger.info("Start main!")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_app())


