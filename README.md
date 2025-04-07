# 🎬 Movie Review API

The **Movie Review API** is a backend system built with FastAPI that allows users to manage movie data and submit reviews. It includes secure user authentication, role-based access control for administrators, and real-time average score calculation for each movie.

Designed with clean architecture and modular components, this API serves as a solid foundation for movie-related applications, from simple review platforms to more complex systems with frontend integration.

---

## 🚀 Features

- 🔐 User registration and login with JWT authentication
- 🎞️ Create, update, and delete movies
- 📝 Authenticated users can post reviews
- ✨ Admins can delete any movie or review
- 📊 Automatically calculates and updates average movie scores
- 🔎 Search movies by name and fetch their reviews

---

## 🧱 Tech Stack

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **JWT (via python-jose)**
- **bcrypt for password hashing**
- **dotenv for environment variable management**

---

## 📂 Endpoints Overview

| Method | Endpoint                  | Description                           |
|--------|---------------------------|---------------------------------------|
| POST   | `/register`               | Register new user                     |
| POST   | `/token`                  | Get JWT token                         |
| GET    | `/movies/`                | Get all movies                        |
| GET    | `/movies/{name}`          | Search movies by name                 |
| POST   | `/movies/`                | Add a new movie                       |
| PATCH  | `/movies/{movie_id}`      | Update movie (auth required)         |
| DELETE | `/movies/{movie_id}`      | Delete movie (admin only)            |
| POST   | `/reviews/`               | Add review to a movie (auth required)|
| GET    | `/movies/{id}/reviews`    | Get all reviews for a movie           |
| PATCH  | `/reviews/{review_id}`    | Update your review                    |
| DELETE | `/reviews/{review_id}`    | Delete review (admin only)            |

---

## 🔒 Authentication

This API uses **Bearer tokens**.  
Use `/token` to obtain a JWT, then click the 🔓 lock icon in Swagger UI to authenticate.

---
