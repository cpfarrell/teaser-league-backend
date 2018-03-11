from datetime import datetime
import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from teaser_league_backend.constants import MLB_TEASER_LEAGUE_NAME
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.league_users import LeagueUsers
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.nfl_db.database_initialization.utils import normalize_username

engine = create_engine('sqlite:///sqlalchemy_example.db', connect_args={'timeout': 75})
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Load the users for our fake MLB league
usernames = [
    'Chris Farrell',
    'Mike Woods',
    'Naman Goyal',
]
for username in usernames:
    session.add(
        LeagueUsers(
            username=username,
            teaser_league_id=MLB_TEASER_LEAGUE_NAME,
        ),
    )
session.commit()
