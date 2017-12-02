from datetime import datetime
import pytz

import nflgame
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from teaser_league_backend.constants import team_name_to_acronym
from teaser_league_backend.constants import week_to_gid
from teaser_league_backend.constants import CURRENT_YEAR
import teaser_league_backend.database_initialization.creator
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek

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

def update_team_score(week, team, score, opponent_score, final):
    team_week = session.query(TeamWeek).filter(and_(TeamWeek.week == week, TeamWeek.team == team)).one()
    team_week.score = score
    team_week.opponent_score = opponent_score
    team_week.game_final = final

def update_scores():
    # Remove the filter if you recreate database to get all past scores.
    for team_week in session.query(TeamWeek)\
            .filter(and_(TeamWeek.game_final == False, TeamWeek.game_time < datetime.now()))\
            .group_by(TeamWeek.week)\
            .all():
        for game in nflgame.games(CURRENT_YEAR, week=team_week.week):
            update_team_score(week=team_week.week, team=game.home, score=game.score_home, opponent_score=game.score_away, final=game.game_over())
            update_team_score(week=team_week.week, team=game.away, score=game.score_away, opponent_score=game.score_home, final=game.game_over())

    session.commit()

update_scores()

