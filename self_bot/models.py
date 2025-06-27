from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(Text, nullable=False)
    reply_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)



