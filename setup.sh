set -e

virtualenv virtualenv_run
source virtualenv_run/bin/activate
pip install -r requirements.txt
export FLASK_APP=teaser_league_backend/webapp.py
