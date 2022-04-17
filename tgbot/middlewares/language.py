from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.user import User


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, data):
        user = types.User.get_current()
        session: AsyncSession = data[-1]['session']
        data = await session.execute(select(User.language).filter(User.user_id == user.id))
        if data:
            return data.scalar()
        else:
            return user.locale