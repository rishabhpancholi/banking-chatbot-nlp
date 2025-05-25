from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal,engine
from helper import get_response
import models   
import joblib
import json

#Initializing the app
app = FastAPI()

#Cross origin resource sharing
origins=['http://localhost:8502']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
)

#Creating a Chat class
class Chat(BaseModel):
  user_input: str
  chatbot_response: Optional[str] = None

# Creating a User class
class User(BaseModel):
  username: str
  password: str 
  chats: Optional[List[Chat]]=None

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all the tables
models.Base.metadata.create_all(bind=engine)


#Loading the model and data:
with open('artifacts/chatbot.pkl','rb') as f:
    chatbot_model = joblib.load(f)

with open('artifacts/classes.pkl','rb') as f:
    intent_classes = joblib.load(f)

with open('artifacts/responses.json','r') as f:
    responses = json.load(f)

with open('artifacts/count_vectorizer.pkl','rb') as f:
    cv = joblib.load(f)   

# Login route checking username
@app.post('/login')
def login(user:User,db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username==user.username).first()

    if not db_user:
        raise HTTPException(status_code = 401,detail = 'Invalid username or password')
    
    if user.password!=db_user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    user_chats = []
    for chat in db_user.chats:
       user_chats.append(
       {
           "user_input": chat.user_input,
           "chatbot_response": chat.chatbot_response
       })

    return {'user_chats':user_chats}

# Signup route
@app.post('/signup')
def signup(user:User,db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username==user.username).first()

    if db_user:
        raise HTTPException(status_code = 400, detail="Username not available")
    
    password = user.password
    new_user = models.User(
        username = user.username,
        password = password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{'username': new_user.username}

# Delete Route
@app.delete('/delete')
def delete(user:User,db:Session = Depends(get_db)):
  db_user = db.query(models.User).filter(models.User.username==user.username).first()

  if not db_user:
      raise HTTPException(status_code = 404,detail = "User not found")
  
  db.delete(db_user)
  db.commit()

  return {'message':'Your account is deleted'}
    

#Chat response route
@app.post('/respond')
def respond(user: User, chat: Chat, db:Session = Depends(get_db)):
    username = user.username

    db_user = db.query(models.User).filter(models.User.username == username).first()

    input_message = chat.user_input
    chatbot_response = get_response(input_message,chatbot_model,intent_classes,responses,cv)
    chat.chatbot_response = chatbot_response

    db_chat = models.ChatHistory(
        user_input = chat.user_input,
        chatbot_response = chat.chatbot_response,
        user = db_user
    ) 
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return {'message':f'{chatbot_response}'}
    
