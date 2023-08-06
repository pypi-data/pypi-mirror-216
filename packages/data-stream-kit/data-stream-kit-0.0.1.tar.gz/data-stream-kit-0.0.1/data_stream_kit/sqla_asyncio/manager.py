# -*- coding:utf-8 -*-

# @Time   : 2023/6/25 13:41
# @Author : huangkewei

import asyncio
import typing
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def atomic_session(scoped_session, autocommit=False) -> typing.AsyncIterator[AsyncSession]:
    async with scoped_session() as session:
        try:

            yield session
            if autocommit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise


class AIOSessionManager:
    def __init__(self, url,
                 future=True,
                 pool_size=10,
                 max_overflow=20,
                 pool_recycle=3600,
                 pool_pre_ping=False,
                 pool_reset_on_return=None,
                 echo=False,
                 # autocommit=False,
                 **kwargs):
        self._async_engine = None
        self._Session = self.get_session(
            url,
            future=future,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            pool_pre_ping=pool_pre_ping,
            pool_reset_on_return=pool_reset_on_return,
            echo=echo,
            **kwargs
        )

    def get_session(self, db_uri, **kwargs):
        self._async_engine = create_async_engine(db_uri, **kwargs)
        _async_session_factory = sessionmaker(self._async_engine, class_=AsyncSession, expire_on_commit=False)

        _get_session = async_scoped_session(_async_session_factory, scopefunc=asyncio.current_task)

        return _get_session

    def __call__(self, *args, **kwargs):
        return self._Session()


