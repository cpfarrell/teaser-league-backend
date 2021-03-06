import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base


class Leagues(Base):
    __tablename__ = 'leagues'
    teaser_league_id = Column(String(100), primary_key=True)
    sports_league = Column(String(25), nullable=False)
    sports_year = Column(Integer, nullable=False)
