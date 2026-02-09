from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    media: Mapped[list["Media"]] = relationship("Media", back_populates="user")

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites],
            "comments": [c.serialize() for c in self.comments],
            "media": [m.serialize() for m in self.media]
        }


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(120))
    population: Mapped[int] = mapped_column(Integer)
    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="planet")

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "media": [m.serialize() for m in self.media]
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(50))
    birth_year: Mapped[str] = mapped_column(String(20))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="character")

    planet: Mapped["Planet"] = relationship("Planet")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "planet": self.planet.serialize() if self.planet else None,
            "media": [m.serialize() for m in self.media]
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="comments")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")

    comments: Mapped[list["PostComment"]] = relationship(
        "PostComment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "comments": [c.serialize() for c in self.comments],
            "media": [m.serialize() for m in self.media]
        }



class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(
        String(250), nullable=False)   # path or URL to the file
    # e.g., "image", "video", "audio"
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)

    # Optional foreign keys to link media to posts, users, characters, or planets
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="media")
    user: Mapped["User"] = relationship("User", back_populates="media")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="media")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "description": self.description,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }
