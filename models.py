from sqlalchemy import Column, Integer, String, Text
from database import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String, unique=True, nullable=False, index=True)
    title = Column(String)
    author = Column(String)
    text = Column(Text)
    parent_id = Column(String, nullable=True, index=True)