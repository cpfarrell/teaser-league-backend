import datetime
import pytz

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from teaser_league_backend.constants import week_to_gid
from teaser_league_backend.constants import team_name_to_acronym
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.picks import Picks

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

all_insertable_rows = []
for week, gid in week_to_gid.items():
    response = requests.get('https://docs.google.com/spreadsheets/d/1Toaij3ONlMAVtIXKAkYuRpTagH_Fbj-njx4SArRlRGI/export?gid={}&format=tsv'.format(gid))
    rows = response.text.split('\n')
    possible_pick_rows_string = rows[5:]
    possible_pick_rows = [row.split('\t') for row in possible_pick_rows_string]
    first_non_pick_row = min([i for i, row in enumerate(possible_pick_rows) if row[12]==''])
    pick_rows = possible_pick_rows[:first_non_pick_row]

    for pick_row in pick_rows:
        username =  pick_row[12]

        for pick_index in range(14, 18):
            full_string = pick_row[pick_index]
            if full_string != '':
                team_string = full_string[:full_string.index('@') - 1]            
                team_acronym = team_name_to_acronym[team_string]

                # This is one piece of bad data in the spreadsheets...
                if username == 'Ravi & Brad' and week == 2 and pick_index == 16: 
                    team_acronym = 'DET'

                all_insertable_rows.append(
                    Picks(
                        username=username,
                        week=week,
                        team=team_acronym,
                    )
                )

for row in all_insertable_rows:
    session.add(row)
    session.commit()