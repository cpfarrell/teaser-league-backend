To run project. Need to have python and virtualenv installed (pip install virtualenv). Then run

virtualenv virtualenv_run  
'source virtualenv_run/bin/activate  
pip install -r requirements.txt  
export FLASK_APP=teaser_league_backend/webapp.py  
make start-dev  

Example curls:  
curl http://127.0.0.1:5000/leaderboard  
curl http://127.0.0.1:5000/list_of_weeks/username  
curl http://127.0.0.1:5000/weekly_picks/2/username  
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/make_picks/2/username -d '["GB", "SF"]'  