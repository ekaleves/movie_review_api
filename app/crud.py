from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import and_
from datetime import date
from app.models import User
from app.security import hash_password, verify_password


def create_movie(db: Session, movie_data: schemas.MovieCreate):
    new_movie = models.Movie(**movie_data.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def get_movies(db: Session):
    return db.query(models.Movie).all()


def get_movie_by_name_single(db: Session, name: str):
    return db.query(models.Movie).filter(models.Movie.movie_name == name).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_movie_by_name(db: Session, movie_name: str):
    return db.query(models.Movie).filter(models.Movie.movie_name.ilike(f"%{movie_name}%")).all()


def create_review(db: Session, review_data: schemas.ReviewCreate):
    new_review = models.Review(**review_data.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def partial_update_review(db: Session, review_id: int, review_data: schemas.ReviewUpdate):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        return None

    for key, value in review_data.dict(exclude_unset=True).items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)
    return review


def get_reviews_by_movie_id(db: Session, movie_id: int):
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).all()


def create_user(db: Session, user_data: schemas.UserCreate):
    hashed_pw = hash_password(user_data.password)
    new_user = models.User(
        username=user_data.username,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



