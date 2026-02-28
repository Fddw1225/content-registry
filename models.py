from sqlalchemy import Column, Integer, String, Text
from database import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String, unique=True)
    title = Column(String)
    author = Column(String)
    text = Column(Text)