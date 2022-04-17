import asyncio
import logging

import gspread_asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.content import register_states
from tgbot.handlers.query_handlers import register_callbacks
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbSessionMiddleware
from tgbot.middlewares.language import ACLMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.services.req_func import make_connection_string

logger = logging.getLogger(__name__)


async def create_pool(user, password, database, host, port, echo):
    engine = create_async_engine(
        make_connection_string(async_fallback=True, user=user, password=password, database=database, host=host, port=port),
        future=True,
        echo=echo,
        pool_size=50,
        max_overflow=50
    )
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return db_pool


async def main():
    logging.basicConfig(
        level=logging.DEBUG
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    google_client_manager = gspread_asyncio.AsyncioGspreadClientManager(
        config.misc.scoped_credentials
    )
    bot['config'] = config
    bot['google_client_manager'] = google_client_manager

    dp.middleware.setup(DbSessionMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.middleware.setup(ACLMiddleware(domain="messages", path="locales"))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    # register_admin(dp)
    register_user(dp)
    register_callbacks(dp)
    register_states(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
