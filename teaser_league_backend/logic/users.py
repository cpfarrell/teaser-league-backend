import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base


class Users(Base):
    __tablename__ = 'users'
    username = Column(String(100), primary_key=True)
    password = Column(String(100), primary_key=True)
