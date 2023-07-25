from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from ..database import get_db

# create an API router
router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

# How fastAPI works:
# request send to API server-> searches all sort of path operations and the first match is found(stop running the code)
# request get method url: "/", remember order matters


@router.get("/", response_model=List[schemas.PostOut])  # for retrieving data
def get_posts(db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):  # PERFORMS SQL OPERATIONS
    db_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(
        limit).offset(skip).all()
    return db_posts  # automatically converts to json


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# new_post stores it as a pydantic model and it has a method called .dict to convert it to dictionary so that we can store it in our global array in json format.
def create_posts(new_post: schemas.CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=curr_user.id, **new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
# validate it if it can be converted to a integer. and automatically converts it to an integer
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""Select * from posts where id = %s """, (str(id),))
    # return_post = cur.fetchone()

    # sql alchemy code:
    fetch_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id -> {id} was not found")

    return fetch_post


# remember path order matters. So @app.get("/posts/latest") can be confused with @app.get("/posts/{id}"). So the id can be -> latest .So it validates the @app.get("/posts/{id}").


# delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # sql alchemy code
    post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID : {id} does not exist")

    if deleted_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@router.put("/{id}", response_model=schemas.Post)
# getting the post schema
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # SQL ALCHEMY CODE:
    update_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_post.first()  # grab the specific post
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID : {id} does not exist")

    if updated_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform requested action")

    update_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_post.first()
