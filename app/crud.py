from sqlalchemy.orm import Session
from app import models, schemas
from app.models import User
from app.security import hash_password, verify_password
from datetime import datetime, timedelta
from fastapi import HTTPException


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

    # Update average score
    update_average_score(db, new_review.movie_id)

    return new_review


def partial_update_review(
        db: Session,
        review_id: int,
        review_data: schemas.ReviewUpdate,
        current_user: User
):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        return None

    # Admin can always update
    if not current_user.is_admin:
        # Only the owner can edit
        if review.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this review.")

    # Only allow if within 30 minutes
    now = datetime.utcnow()
    if (now - review.created_at).total_seconds() > 1800:
        raise HTTPException(status_code=403, detail="You can only edit a review within 30 minutes of posting.")

    for key, value in review_data.dict(exclude_unset=True).items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    # Update average score
    update_average_score(db, review.movie_id)

    return review


def partial_updated_movie(db: Session, movie_id: int, movie_data: schemas.MovieUpdate, current_user: User):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found.")

    time_diff = datetime.utcnow() - movie.created_at
    if time_diff > timedelta(minutes=30):
        raise HTTPException(status_code=403, detail="You can only edit a movie within 30 minutes of posting.")

    for key, value in movie_data.dict(exclude_unset=True).items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


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


def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully."}


def delete_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfuly"}


def update_average_score(db: Session, movie_id: int):
    reviews = db.query(models.Review).filter(models.Review.movie_id == movie_id).all()

    if not reviews:
        return

    average = sum(review.score for review in reviews) / len(reviews)

    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        movie.average_score = round(average, 2)
        db.commit()



