import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base 


class UserWeekResult(Base):
    __tablename__ = 'user_week_result'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    teaser_league_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, primary_key=True)
    week = Column(Integer, nullable=False, primary_key=True)
    won_loss = Column(Float, nullable=False)
