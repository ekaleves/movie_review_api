from pydantic import BaseModel
from datetime import date
from typing import Optional


class MovieBase(BaseModel):
    movie_name: str
    movie_year: int
    description: str
    genre: str
    writers: Optional[str] = None
    actors: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieConfig(MovieBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class ReviewBase(BaseModel):
    review_text: str
    score: float


class ReviewCreate(ReviewBase):
    review_text: str
    score: float
    movie_id: int
    user_id: Optional[int] = None


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[float] = None


class ReviewConfig(ReviewBase):
    id: int
    movie_id: int
    user_id: Optional[int]
    review_date: Optional[date]

    model_config = {
        "from_attributes": True
    }


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }



