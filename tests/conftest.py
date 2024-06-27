import sys
import os
print('start=========')

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import close_all_sessions

from app.main import app
from app.database import get_db
from app.api.models import Base

# テスト対象のアプリケーションディレクトリを取得
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")
sys.path.insert(0, app_dir)


class TestingSession(AsyncSession):
    async def commit(self):
        # テストのため永続化しない
        await self.flush()
        await self.expire_all()


@pytest.fixture(scope="function")
async def test_db():
    engine = create_async_engine("sqlite:///./sql_app_test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(
        class_=TestingSession, autocommit=False, autoflush=False, bind=engine
    )

    db = TestSessionLocal()

    async def get_db_for_test():
        try:
            yield db
            await db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            await db.rollback()

    app.dependency_overrides[get_db] = get_db_for_test

    # テストケース実行
    yield db

    await db.rollback()
    await close_all_sessions()
    await engine.dispose()