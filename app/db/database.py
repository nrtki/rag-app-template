from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. 非同期エンジンの作成
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. DBセッションの作成（DBとの会話の窓口）
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 3. モデル定義の親クラス
Base = declarative_base()

# 4. 依存性注入用関数（FastAPIで後で使います）
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session