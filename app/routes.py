from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from fastapi import HTTPException
from typing import List
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token
from app.crud import authenticate_user
from datetime import timedelta
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()


@router.post("/movies/", response_model=schemas.MovieBase)
def created_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)


@router.get("/movies/", response_model=List[schemas.MovieBase])
def read_all_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)


@router.post("/reviews/", response_model=schemas.ReviewConfig)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movie = db.query(models.Movie).filter(models.Movie.id == review.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    review_data = review.dict()
    review_data["user_id"] = current_user.id

    return crud.create_review(db, schemas.ReviewCreate(**review_data))


@router.get("/movies/{name}", response_model=List[schemas.MovieConfig])
def read_movie_by_name(name: str, db: Session = Depends(get_db)):
    movies = crud.get_movie_by_name(db, name)
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")
    return movies


@router.get("/movies/{movie_id}/reviews", response_model=List[schemas.ReviewConfig])
def read_reviews_by_movie_id(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_by_movie_id(db, movie_id)


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken."
        )
    return crud.create_user(db, user)


@router.post("/token")
def login_for_access_toke(
        from_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, from_data.username, from_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.patch("/reviews/{review_id}", response_model=schemas.ReviewConfig)
def update_review(
        review_id: int,
        review_data: schemas.ReviewUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    updated = crud.partial_update_review(db, review_id, review_data, current_user)  # type: ignore
    if updated is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    return updated


@router.patch("/movies/{movie_id}", response_model=schemas.MovieConfig)
def update_movie(
        movie_id: int,
        movie_data: schemas.MovieUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return crud.partial_updated_movie(db, movie_id, movie_data, current_user)


@router.delete("/reviews/{review_id}")
def delete_review(
        review_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only Administrator users can delete reviews.")
    return crud.delete_review(db, review_id)


@router.delete("/movies/{movie_id}")
def delete_movie(
        movie_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only Administrator users can delete movies.")
    return crud.delete_movie(db, movie_id)





