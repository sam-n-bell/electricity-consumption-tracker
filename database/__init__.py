import contextlib
from dataclasses import dataclass
from typing import Any, AsyncIterator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

import settings

logger = structlog.get_logger("eleconsurp")


@dataclass
class DatabaseConfig:
    dialect: str
    user: str
    password: str
    host: str
    port: str
    db: str

    @property
    def connection_str(self) -> str:
        return (
            f"{self.dialect}://"
            f"{self.user}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.db}"
            # "?sslmode=require"
            # "&sslrootcert=/usr/src/app/database/ca-certificate.crt"
        )


def get_postgres_conn_str():
    return DatabaseConfig(
        settings.PG_DIALECT,
        settings.PG_USER,
        settings.PG_PWD,
        settings.PG_HOST,
        settings.PG_PORT,
        settings.PG_DB,
    ).connection_str


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# 'sslmode': 'require',
#         'sslrootcert': ca_cert_path

sessionmanager = DatabaseSessionManager(get_postgres_conn_str(), {"echo": True})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


def validate_db_connection(db_session: Session, database_name: str = None):
    try:
        return db_session.is_active
    except Exception as e:
        logger.error(
            "validate_db_connection_exception", db_name=database_name, error=str(e)
        )
        return False
