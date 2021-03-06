import pprint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import exists

from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.logic.users import Users
from teaser_league_backend.webapp import busted
from teaser_league_backend.webapp import get_won_loss_for_week
from teaser_league_backend.webapp import get_busted_string
from teaser_league_backend.logic.league_users import LeagueUsers

pp = pprint.PrettyPrinter(indent=4)

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

#print(session.query(Users).filter(Users.username=='Chris Farrell').filter(Users.password=='pChris Farrell').count())

#scores = []
#for username, in session.query(Picks.username).distinct():
#    total_points = 0
#    for week, in session.query(TeamWeek.week).distinct().order_by(TeamWeek.week):
#        total_points += get_won_loss_for_week(week, username)
#    scores.append({'username': username, 'points': total_points})
#pp.pprint(sorted(scores, key=lambda k: k['points'], reverse=True))

#teams = []
#for team_week in session.query(TeamWeek).filter(TeamWeek.week == 16).filter(TeamWeek.team == 'CAR'):
#   get_busted_string(team_week)
#   teams.append({'team': team_week.team, 'busted_string': get_busted_string(team_week)})
#pp.pprint(teams)

users = [user for user in session.query(LeagueUsers)]
import ipdb; ipdb.set_trace()
pass

#for result in session.query(TeamWeek, Picks)\
#                        .outerjoin(Picks, and_(Picks.team==TeamWeek.team, Picks.week==TeamWeek.week))\
#                        .order_by(TeamWeek.game_time, TeamWeek.game_id)\
#                        .all():
#    print(str(result.TeamWeek.team) + " " + str(result.TeamWeek.game_time))

#only_final=False
#print [loser.username for loser in session.query(Picks.username)\
#        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
#        .filter(TeamWeek.week == 13)\
#        .filter(busted(TeamWeek))\
#        .filter(or_(TeamWeek.game_final, not only_final))
#        .distinct()\
#        .all()]
