from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from .database import get_db
from cryp import schemas,models, utils
# from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn 
# Load environment variables from the .env file
# load_dotenv()
router = APIRouter(
    prefix="/users",
    tags=['Users']
)
# app = FastAPI() 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)