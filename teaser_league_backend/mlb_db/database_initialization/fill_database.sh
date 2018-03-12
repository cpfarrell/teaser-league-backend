#!/bin/bash
set -euxo pipefail

# python -m teaser_league_backend.mlb_db.database_initialization.load_users
# python -m teaser_league_backend.mlb_db.database_initialization.fill_accounts_for_fake_mlb
python -m teaser_league_backend.mlb_db.database_initialization.load_games
