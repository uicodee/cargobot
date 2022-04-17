from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey

from tgbot.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), autoincrement=True, nullable=False, primary_key=True)
    user_id = Column(BigInteger(), primary_key=True, nullable=False)
    language = Column(String(length=20), nullable=False)

    def __str__(self):
        return f"{self.id} | {self.user_id} | {self.language}"