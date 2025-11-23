from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base, get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db import models 
from pydantic import BaseModel 
from app.db.models import Document
from app.utils.gemini import get_embedding, generate_answer

app = FastAPI()
# CORS設定
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class DocumentSchema(BaseModel):
    content: str
    source: str | None = None
class ChatRequest(BaseModel):
    message: str
# --- 1. ドキュメント登録API (本物のベクトル化) ---
@app.post("/documents")
async def create_document(doc: DocumentSchema, db: AsyncSession = Depends(get_db)):
    try:
        # Geminiを使ってテキストをベクトル化 (768次元)
        vector = await get_embedding(doc.content)

        new_doc = Document(
            content=doc.content,
            source=doc.source,
            embedding=vector
        )
        
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)
        
        return {"id": new_doc.id, "status": "saved"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
# リクエストの型定義
class ChatRequest(BaseModel):
    message:str
@app.post("/chat")
async def chat(req:ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 1. 質問文をベクトル化
        query_vector = await get_embedding(req.message)
        
        # 2. ベクトル検索 (コサイン類似度で近い順に3件取得)
        # Document.embedding は pgvector のカラム
        stmt = select(Document).order_by(
            Document.embedding.cosine_distance(query_vector)
        ).limit(3)
        
        results = await db.execute(stmt)
        documents = results.scalars().all()
        
        # 3. 検索結果（コンテキスト）を結合
        if not documents:
            context = "参考情報はありません。"
        else:
            context = "\n\n".join([f"- {d.content} (出典: {d.source})" for d in documents])
        
        print(f"🔍 検索ヒット: {len(documents)}件") # ログ確認用
        
        # 4. LLMに回答生成させる
        answer = await generate_answer(req.message, context)
        
        return {"reply": answer}
        
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "申し訳ありません。エラーが発生しました。"}
# アプリ起動時にテーブルを自動作成する処理
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # まず pgvector (vector) 拡張を作成しておく
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        # DBにテーブルが無ければ作成する
        await conn.run_sync(Base.metadata.create_all)
    print("----------------------------------")
    print(" DB connection & Tables created!! ")
    print("----------------------------------")

@app.get("/")
async def root():
    return {"message": "Hello, RAG App!"}