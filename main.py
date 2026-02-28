from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib
import unicodedata

from database import engine, SessionLocal, Base
from models import Content

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 输入模型
class ContentInput(BaseModel):
    title: str
    text: str
    author: str | None = None
    parent_id: str | None = None

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 内容规范化
def canonicalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip()
    return text

# 生成内容 ID
def generate_content_id(text: str) -> str:
    if text is None:
        raise ValueError("Text cannot be None")
    normalized = canonicalize(text)
    return "cx-" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]

# 根接口
@app.get("/")
def root():
    return {"status": "registry running"}

# 注册内容
@app.post("/register")
def register(content: ContentInput, db: Session = Depends(get_db)):
    cid = generate_content_id(content.text)

    # 检查是否已注册
    existing = db.query(Content).filter(Content.content_id == cid).first()
    if existing:
        return {"content_id": cid, "note": "already registered"}

    # 创建数据库对象
    content_db = Content(
        content_id=cid,
        title=content.title,
        author=content.author,
        text=content.text,
        parent_id=content.parent_id
    )

    db.add(content_db)
    db.commit()
    db.refresh(content_db)

    return {"content_id": cid}

# 查询内容
@app.get("/content/{cid}")
def get_content(cid: str, db: Session = Depends(get_db)):
    result = db.query(Content).filter(Content.content_id == cid).first()

    if not result:
        raise HTTPException(status_code=404)

    return {
        "content_id": result.content_id,
        "title": result.title,
        "author": result.author,
        "text": result.text,
        "parent_id": result.parent_id
    }