from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_

from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek
from teaser_league_backend.logic.game import Game
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.logic.user_week_result import UserWeekResult

engine = create_engine('sqlite:///sqlalchemy_example.db')

Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy import all_

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

#session.query(Picks).filter(Picks.username=='farrell').filter(Picks.week==1).delete()
#for team in [u'SF', u'GB']:
#    session.add(Picks(username='farrell', team=team, week=1))
#session.commit()

#                        .filter(TeamWeek.busted == False)\
#                        .join(Picks, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
#                        .filter(TeamWeek.week == 1)\

#                        .filter(TeamWeek.busted == True)\

print(session.query(Picks.username)\
              .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
              .filter(Picks.username == 'Chris Farrell')\
              .filter(TeamWeek.week == 2)\
              .filter(TeamWeek.busted == True)\
              .count())

