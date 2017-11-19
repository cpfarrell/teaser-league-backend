from datetime import datetime
import pytz

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek
from teaser_league_backend.logic.game import Game
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.logic.user_week_result import UserWeekResult
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
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
  
eastern = pytz.timezone("America/New_York")

# Insert the team weeks
team_week1 = TeamWeek(id=0, week=1, team='SF', vegas_spread=6, adjusted_spread=20, game_time=datetime(2017, 11, 16, 19, 55, 0, 0, eastern), score=35, busted=False)
team_week2 = TeamWeek(id=1, week=1, team='SEA', vegas_spread=-6, adjusted_spread=8, game_time=datetime(2017, 11, 16, 19, 55, 0, 0, eastern), score=7, busted=True)
team_week3 = TeamWeek(id=2, week=1, team='WAS', vegas_spread=-3, adjusted_spread=11, game_time=datetime(2017, 11, 19, 12, 55, 0, 0, eastern), score=17, busted=False)
team_week4 = TeamWeek(id=3, week=1, team='GB', vegas_spread=3, adjusted_spread=17, game_time=datetime(2017, 11, 19, 12, 55, 0, 0, eastern), score=14, busted=False)
team_week5 = TeamWeek(id=4, week=2, team='GB', vegas_spread=6, adjusted_spread=20, game_time=datetime(2017, 11, 23, 19, 55, 0, 0, eastern))
team_week6 = TeamWeek(id=5, week=2, team='SEA', vegas_spread=-6, adjusted_spread=8, game_time=datetime(2017, 11, 23, 19, 55, 0, 0, eastern))
team_week7 = TeamWeek(id=6, week=2, team='WAS', vegas_spread=-13, adjusted_spread=1, game_time=datetime(2017, 11, 26, 12, 55, 0, 0, eastern))
team_week8 = TeamWeek(id=7, week=2, team='SF', vegas_spread=13, adjusted_spread=27, game_time=datetime(2017, 11, 26, 12, 55, 0, 0, eastern))
session.add(team_week1)
session.add(team_week2)
session.add(team_week3)
session.add(team_week4)
session.add(team_week5)
session.add(team_week6)
session.add(team_week7)
session.add(team_week8)

# Insert some games.
game1 = Game(id=0, home_team='SF', away_team='SEA', week=1)
game2 = Game(id=1, home_team='WAS', away_team='GB', week=1)
game3 = Game(id=2, home_team='GB', away_team='SEA', week=2)
game4 = Game(id=3, home_team='SWAS', away_team='SF', week=2)
session.add(game1)
session.add(game2)
session.add(game3)
session.add(game4)

# Insert some user week results.
utr_farrell_1 = UserWeekResult(username='farrell', week=1, won_loss=200)
utr_farrell_2 = UserWeekResult(username='farrell', week=2, won_loss=300)
utr_farrell_3 = UserWeekResult(username='farrell', week=3, won_loss=-500)
utr_woods_1 = UserWeekResult(username='woods', week=1, won_loss=-100)
utr_woods_2 = UserWeekResult(username='woods', week=2, won_loss=-400)
utr_woods_3 = UserWeekResult(username='woods', week=3, won_loss=200)
utr_ngoyal_1 = UserWeekResult(username='ngoyal', week=1, won_loss=150)
utr_ngoyal_2 = UserWeekResult(username='ngoyal', week=2, won_loss=600)
utr_ngoyal_3 = UserWeekResult(username='ngoyal', week=3, won_loss=-300)
session.add(utr_farrell_1)
session.add(utr_farrell_2)
session.add(utr_farrell_3)
session.add(utr_woods_1)
session.add(utr_woods_2)
session.add(utr_woods_3)
session.add(utr_ngoyal_1)
session.add(utr_ngoyal_2)
session.add(utr_ngoyal_3)

picks = [
    Picks(username='farrell', team='SF', week=1),
    Picks(username='farrell', team='GB', week=1),
    Picks(username='woods', team='SEA', week=1),
    Picks(username='ngoyal', team='WAS', week=1),
    Picks(username='farrell', team='WAS', week=2),
    Picks(username='woods', team='GB', week=2),
]
for pick in picks:
    session.add(pick)

# Commit everything
session.commit()
