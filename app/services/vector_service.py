from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Document
# ※以下はOpenAIの呼び出し（疑似コード）
# from app.utils.openai import get_embedding 

class VectorService:
    def __init__(self, db: Session):
        self.db = db

    # 【保存】Webから来たデータをDBに入れる
    async def add_document(self, text: str, source: str):
        # 1. テキストをAIでベクトル変換（[0.12, 0.54, ...]のような数値配列）
        # vector = await get_embedding(text) 
        # ここではダミーで埋めます
        vector = [0.0] * 1536 

        # 2. Pythonのオブジェクトを作成
        new_doc = Document(
            content=text,
            embedding=vector,
            source=source
        )

        # 3. DBセッションに追加してコミット（確定）
        self.db.add(new_doc)
        self.db.commit()
        self.db.refresh(new_doc)
        return new_doc

    # 【検索】Webからの質問に近いデータをDBから探す
    async def search_similar(self, query_text: str, limit: int = 3):
        # 1. 質問文をベクトル変換
        # query_vector = await get_embedding(query_text)
        query_vector = [0.0] * 1536 # ダミー

        # 2. ベクトル検索のSQLを構築（ここが肝！）
        # embeddingカラムとquery_vectorの「コサイン距離」が近い順に並べる
        stmt = select(Document).order_by(
            Document.embedding.cosine_distance(query_vector)
        ).limit(limit)

        # 3. 実行して結果取得
        result = self.db.execute(stmt)
        return result.scalars().all()