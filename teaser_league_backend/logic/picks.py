# Table containing everyone's picks
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base


class Picks(Base):
    __tablename__ = 'picks'
    teaser_league_id = Column(Integer, primary_key=True)
    username = Column(String(50), primary_key=True)
    week = Column(Integer, primary_key=True)
    team = Column(String(25), primary_key=True)
