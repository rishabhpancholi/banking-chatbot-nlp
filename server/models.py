from sqlalchemy import Column,Integer,String ,Text,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# User Table
class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    chats = relationship("ChatHistory",back_populates="user")


# Chat History Table
class ChatHistory(Base):
    __tablename__='chat_history'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    user_input = Column(Text)
    chatbot_response = Column(Text)

    user = relationship("User",back_populates="chats")
