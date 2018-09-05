#!/bin/bash
set -euxo pipefail

python -m teaser_league_backend.database_initialization.creator
python -m teaser_league_backend.database_initialization.pull_games_from_spreadsheets
python -m teaser_league_backend.database_initialization.pull_picks_from_spreadsheets
python virtualenv_run/lib/python2.7/site-packages/nflgame/update_sched.py --year=2018
python -m teaser_league_backend.database_update.update_game_scores --pull-all
python -m teaser_league_backend.database_initialization.fill_accounts_table
