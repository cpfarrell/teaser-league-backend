import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base


class LeagueUsers(Base):
    __tablename__ = 'league_users'
    teaser_league_id = Column(String(100), primary_key=True)
    username = Column(String(100), nullable=False, primary_key=True)
