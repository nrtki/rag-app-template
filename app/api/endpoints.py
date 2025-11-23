from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.vector_service import VectorService
from pydantic import BaseModel

router = APIRouter()

# リクエストボディの定義
class DocumentCreate(BaseModel):
    text: str
    source: str

@router.post("/documents/")
async def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    service = VectorService(db)
    # ここで「DB保存処理」を呼び出す
    saved_doc = await service.add_document(doc.text, doc.source)
    return {"status": "success", "id": saved_doc.id}

@router.get("/search/")
async def search_documents(query: str, db: Session = Depends(get_db)):
    service = VectorService(db)
    # ここで「DB検索処理」を呼び出す
    results = await service.search_similar(query)
    return {"results": [r.content for r in results]}