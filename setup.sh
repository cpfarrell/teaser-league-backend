set -e

virtualenv --python=python2.7 virtualenv_run
source virtualenv_run/bin/activate
pip install -r requirements.txt
export FLASK_APP=teaser_league_backend/webapp.py
