from sqlalchemy import (Column, Integer, Float, String, Date,
                        Text, ForeignKey, DateTime, Boolean)
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    movie_name = Column(String, nullable=False)
    movie_year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    genre = Column(String, nullable=False)
    writers = Column(Text, nullable=True)
    actors = Column(Text, nullable=True)
    average_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow())

    reviews = relationship("Review", back_populates="movie", cascade="all, delete")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_text = Column(Text, nullable=False)
    review_date = Column(Date, default=datetime.utcnow)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    movie = relationship("Movie", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    reviews = relationship("Review", back_populates="user")
