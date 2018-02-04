import os
from sqlalchemy import create_engine

from teaser_league_backend.logic.base import Base
import teaser_league_backend.logic.league_users
import teaser_league_backend.logic.leagues
import teaser_league_backend.logic.team_week
import teaser_league_backend.logic.picks
import teaser_league_backend.logic.users

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db', connect_args={'timeout': 75})
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
