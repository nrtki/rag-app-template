from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector  # pgvector用ライブラリ
from app.db.database import Base

EMBEDDING_DIMENSION = 768  # OpenAIのEmbeddingモデルの次元数
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # 元のテキスト内容
    # OpenAIのEmbeddingモデル(text-embedding-3-small)は1536次元
    embedding = Column(Vector(EMBEDDING_DIMENSION)) 
    source = Column(String, nullable=True)  # 出典（ファイル名など）