from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import and_

from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek
from teaser_league_backend.logic.game import Game
from teaser_league_backend.logic.user_week_result import UserWeekResult

import teaser_league_backend.logic.team_week
from teaser_league_backend.logic.picks import Picks

app = Flask(__name__)

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


@app.route('/leaderboard')
def leaderboard():
    scores = []
    for total in session.query(UserWeekResult.username, func.sum(UserWeekResult.won_loss)).group_by(
            UserWeekResult.username).order_by(func.sum(UserWeekResult.won_loss).desc()).all():
        scores.append({'username': total.username, 'profit': total[1]})
    return jsonify(scores)

@app.route('/list_of_weeks/<username>')
def list_of_weeks(username):
    weeks = []
    for uwr in session.query(UserWeekResult).filter(UserWeekResult.username == username).all():
        weeks.append({'week': uwr.week, 'profit': uwr.won_loss})
    return jsonify(weeks)

@app.route('/weekly_picks/<week>/<username>')
def week_breakdown(week, username):
    teams = []
    for result in session.query(TeamWeek, Picks)\
                        .outerjoin(Picks, and_(Picks.team==TeamWeek.team, Picks.week==TeamWeek.week, Picks.username==username))\
                        .filter(TeamWeek.week==week)\
                        .all():
        teams.append(
            {
                'team': result.TeamWeek.team,
                'game_time': str(result.TeamWeek.game_time),
                'spread': result.TeamWeek.adjusted_spread,
                'pick': '' if result.Picks is None else 'X',
                'score': result.TeamWeek.score,
                'busted': 'X' if result.TeamWeek.busted else '',
                'locked': result.TeamWeek.game_time < datetime.now()
            }
        )
    return jsonify(teams)

@app.route('/make_picks/<week>/<username>', methods = ['POST'])
def make_picks(week, username):
    session.query(Picks).filter(Picks.username==username).filter(Picks.week==week).delete()
    teams = request.get_json()
    print("Making picks " + str(teams))
    for team in teams:
        session.add(Picks(username=username, team=team, week=week))
    session.commit()
    return jsonify({'success': True})
