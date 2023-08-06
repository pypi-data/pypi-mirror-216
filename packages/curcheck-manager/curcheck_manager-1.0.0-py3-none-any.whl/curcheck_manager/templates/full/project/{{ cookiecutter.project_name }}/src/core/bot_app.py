""" Сборка бота """
from loguru import logger

from curcheck import Dispatcher

from .settings import settings

from ..apps import routers


dp = Dispatcher()


async def start_bot():
    # include routers
    logger.info("Include base_router")
    for router in routers:
        dp.include_router(
            router=router
        )

    logger.info("Start polling")
    await dp.start()
