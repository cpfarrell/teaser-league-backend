import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
from teaser_league_backend.logic.base import Base


class TeamWeek(Base):
    __tablename__ = 'team_week'
    # Here we define columns for the table team_week
    # Notice that each column is also a normal Python instance attribute.
    game_id = Column(String(25), nullable=False)
    week = Column(Integer, nullable=False, primary_key=True)
    team = Column(String(25), nullable=False, primary_key=True)
    vegas_spread = Column(Float, nullable=False)
    adjusted_spread = Column(Float, nullable=False)
    # Both following null if game not yet completed
    covered = Column(Boolean, nullable=True)
    score = Column(Integer, nullable=True)
    game_time = Column(DateTime, nullable=False)
    busted = Column(Boolean, nullable=True)
