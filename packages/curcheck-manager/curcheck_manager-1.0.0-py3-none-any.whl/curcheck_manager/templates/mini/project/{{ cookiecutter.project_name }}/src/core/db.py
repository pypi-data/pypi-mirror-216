""" Сборка базы данных """

from tortoise import Tortoise
from loguru import logger

from .tortoise_orm import TORTOISE_ORM


async def database_init() -> None:
    """
    Initialises ORM.
    """
    logger.debug("Init db")

    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()

