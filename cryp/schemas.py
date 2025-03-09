from pydantic import BaseModel,EmailStr,ConfigDict
# from datetime import datetime
from typing import Optional
MyModelConfig = ConfigDict(arbitrary_types_allowed=True)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    

    model_config = MyModelConfig
class UserCreate(BaseModel):

    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional [str] = None
