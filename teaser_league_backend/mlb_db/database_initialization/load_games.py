import datetime
import pytz

import mlbgame

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from datetime import date
from datetime import timedelta

from teaser_league_backend.constants import NEW_YORK_TIMEZONE
from teaser_league_backend.constants import MLB_LEAGUE_NAME
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek

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

global_id_counter = 0

# First delete all current weeks in database
session.query(TeamWeek).filter(and_(TeamWeek.year==2018, TeamWeek.sports_league==MLB_LEAGUE_NAME)).delete()

start_date = date(2018, 4, 5)
end_date = date(2018, 10, 4)
all_sundays = [start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1) if (start_date + timedelta(days=x)).weekday() == 6]

all_insertable_rows = []
global_id_counter = 0
for week_number, sunday in enumerate(all_sundays):
    games = mlbgame.day(sunday.year, sunday.month, sunday.day)
    for game in games:
        def make_row(game, use_home=True):
            game_time = datetime.datetime.strptime(game.game_start_time, '%I:%M%p')
            game_datetime = game_time.replace(year=sunday.year, month=sunday.month, day=sunday.day)
            localized_gametime = NEW_YORK_TIMEZONE.localize(game_datetime).astimezone(pytz.utc)

            info = {
                'sports_league': MLB_LEAGUE_NAME,
                'game_id': game.game_id,
                'week': week_number,
                'year': 2018,
                'team': game.home_team if use_home else game.away_team,
                'vegas_spread': 0.,
                'adjusted_spread': 2.,
                'game_time': localized_gametime,
                'game_final': False,
            }
#            import ipdb; ipdb.set_trace()
            return info

        all_insertable_rows.append(make_row(game, use_home=True))
        global_id_counter += 1
        all_insertable_rows.append(make_row(game, use_home=False))
        global_id_counter += 1

#import ipdb; ipdb.set_trace()
for row in all_insertable_rows:
    session.add(TeamWeek(**row))

session.commit()
