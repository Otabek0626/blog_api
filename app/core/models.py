from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    is_admin = Column(Boolean, nullable=False, default=False)
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", cascade="all,delete", back_populates="user")
    comments = relationship("Comment", cascade="all,delete", back_populates="user")

    def __str__(self):
        return self.username


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    exercise_type = Column(String, nullable=False)
    post_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now()) 
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="posts")
    photos = relationship("Photo", cascade="all,delete", back_populates="post")
    comments = relationship("Comment", cascade="all,delete", back_populates="post")

    def __str__(self):
        return f"Post(id={self.id}, exercise_type={self.exercise_type}, created_at={self.created_at})"

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    photo_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # Use created_at for ordering
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    post = relationship("Post", back_populates="photos")

    def __str__(self):
        return f"Photo(id={self.id}, post_id={self.post_id}, created_at={self.created_at})"

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    comment_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())  # Use created_at for ordering
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def __str__(self):
        return f"Comment(id={self.id}, post_id={self.post_id}, created_at={self.created_at})"

