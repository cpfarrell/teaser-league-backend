import datetime
import pytz

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teaser_league_backend.constants import team_name_to_acronym
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

week_to_gid = {
    1: '0',
    2: '2141030333',
    3: '62226504'
}

global_id_counter = 0

all_insertable_rows = []
for week, gid in week_to_gid.items():
    response = requests.get('https://docs.google.com/spreadsheets/d/1Toaij3ONlMAVtIXKAkYuRpTagH_Fbj-njx4SArRlRGI/export?gid={}&format=tsv'.format(gid))
    rows = response.text.split('\n')
    possible_team_rows_string = rows[5:]
    possible_team_rows = [row.split('\t') for row in possible_team_rows_string]
    first_non_game_row = min([i for i, row in enumerate(possible_team_rows) if row[2]==''])
    team_rows = possible_team_rows[:first_non_game_row]

    team_dicts = []
    for i, row in enumerate(team_rows):
        road_team_id, home_team_id = [i, i+1] if i%2==0 else [i-1, i]
        full_game_time_string = team_rows[road_team_id][1] + team_rows[home_team_id][1]
        road_team = team_name_to_acronym[team_rows[road_team_id][2]]
        home_team = team_name_to_acronym[team_rows[home_team_id][2]]        
        game_id = '_'.join([road_team, home_team, str(week)])

        team_dicts.append(
            {
                'game_id': global_id_counter,
                'week': week,
                'team': team_name_to_acronym[row[2]],
                'vegas_spread': row[3],
                'adjusted_spread': row[4],
                'game_time': datetime.datetime.strptime(full_game_time_string, '%A, %m/%d %H:%M %p').replace(year=2017),
                'score': row[6],
                # Field from google docs is covered which is the opposite of busted.
                'busted': False if row[7]!='FALSE' else True,
            }
        )
        global_id_counter += 1
    all_insertable_rows.extend(team_dicts)

for row in all_insertable_rows:
    session.add(TeamWeek(**row))

session.commit()
