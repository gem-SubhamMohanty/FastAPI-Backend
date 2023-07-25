from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session

from ..database import get_db

# create a router:
router = APIRouter(
    tags=['Users']
)


# /docs for documentation of api and redoc for another different format of documentation.
# for mysql-> install underline drivers to connect it with sqlalchemy
# for postgresql -> we have drivers psycopg==2.9.1

# for authentication
@router.post("/user_reg", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - retrieve from user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# setting up a router:
@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    rout_user = db.query(models.User).filter(models.User.id == id).first()

    if not rout_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist")
    return rout_user
