from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.users import Users

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

usernames = [
#    'Chris Farrell',
    'Mike Woods',
    'Naman Goyal',
]
for username in usernames:
    session.add(Users(username=username, password=('p' + username)))
session.commit()
