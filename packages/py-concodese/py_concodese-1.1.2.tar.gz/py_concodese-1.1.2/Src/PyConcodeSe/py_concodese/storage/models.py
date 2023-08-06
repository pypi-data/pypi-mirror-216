from __future__ import annotations
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .sql_base import Base
from .filebase import FileBase

# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html


class File(Base, FileBase):
    """represents a source file"""

    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stemmed_name = Column(String)
    package = Column(String)

    extension = Column(String)

    relative_file_path = Column(String)

    identifiers = relationship("Identifier", back_populates="file")

    code_tokens = relationship("Token", back_populates="file")
    comment_tokens = relationship("CommentToken", back_populates="file")

    def __init__(self, name, stemmed_name, package, extension, relative_file_path):
        self.name = name
        self.stemmed_name = stemmed_name
        self.package = package
        self.extension = extension
        self.relative_file_path = relative_file_path


class Identifier(Base):
    """represents an identifier from a file"""
    
    __tablename__ = "identifier"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("file.id"), index=True)
    file = relationship("File", back_populates="identifiers")

    text = Column(String)
    stemmed_text = Column(String)
    tokens = relationship("Token", back_populates="identifier")

    def __init__(self, file, text, stemmed_text):
        self.file = file
        self.text = text
        self.stemmed_text = stemmed_text


class Token(Base):
    """represents a token that was made from an identifier"""
    
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    identifier_id = Column(Integer, ForeignKey("identifier.id"), index=True)
    identifier = relationship("Identifier", back_populates="tokens")
    text = Column(String)
    stemmed_text = Column(String)
    file_id = Column(Integer, ForeignKey("file.id"), index=True)
    file = relationship("File", back_populates="code_tokens")

    def __init__(self, identifier, text, stemmed_text, file):
        self.identifier = identifier
        self.text = text
        self.stemmed_text = stemmed_text
        self.file = file


class CommentToken(Base):
    """represents a token that was made from a comment"""
    __tablename__ = "comment_token"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("file.id"), index=True)
    file = relationship("File", back_populates="comment_tokens")
    text = Column(String)
    stemmed_text = Column(String)

    def __init__(self, file, text, stemmed_text):
        self.file = file
        self.text = text
        self.stemmed_text = stemmed_text
