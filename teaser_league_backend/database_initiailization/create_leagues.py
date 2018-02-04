from datetime import datetime
import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from teaser_league_backend.constants import MAIN_TEASER_LEAGUE_2017_ID 
from teaser_league_backend.constants import NFL_LEAGUE_NAME
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.leagues import Leagues
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.nfl_db.database_initialization.utils import normalize_username

engine = create_engine('sqlite:///sqlalchemy_example.db', connect_args={'timeout': 75})
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.add(Leagues(
    teaser_league_id=MAIN_TEASER_LEAGUE_2017_ID,
    sports_league=NFL_LEAGUE_NAME,
    sports_year= 2017,
))

session.commit()
