
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cryp import user, oauth
from .database import engine
app = FastAPI()
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(oauth.router)
@app.get("/")
def root():
    return {"message": "hello world new okkkk bind "}

