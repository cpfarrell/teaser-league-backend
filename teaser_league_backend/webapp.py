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

WEEKLY_BET = 15

@app.route('/leaderboard')
def leaderboard():
    scores = []
    for username, in session.query(Picks.username).distinct():
        total_profit = 0
        for week, in session.query(TeamWeek.week).distinct().order_by(TeamWeek.week):
            total_profit += get_won_loss_for_week(week, username)
        scores.append({'username': username, 'profit': total_profit})
    return jsonify(sorted(scores, key=lambda k: k['profit'], reverse=True))

@app.route('/list_of_weeks/<username>')
def list_of_weeks(username):
    weeks = []
    for week, in session.query(TeamWeek.week).distinct().order_by(TeamWeek.week):
        weeks.append({'week': week, 'profit': get_won_loss_for_week(week, username)})
    return jsonify(weeks)

@app.route('/weekly_picks/<week>/<username>')
def week_breakdown(week, username):
    teams = []
    for result in session.query(TeamWeek, Picks)\
                        .outerjoin(Picks, and_(Picks.team==TeamWeek.team, Picks.week==TeamWeek.week, Picks.username==username))\
                        .filter(TeamWeek.week==week)\
                        .order_by(TeamWeek.game_time, TeamWeek.game_id)\
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
    for team in teams:
        session.add(Picks(username=username, team=team, week=week))
    session.commit()
    return jsonify({'success': True})

def get_won_loss_for_week(week, username):
    if user_lost_in_week(week, username):
        basic_loss = num_won_in_week(week) * WEEKLY_BET * -1
        return basic_loss + (20 * penalty_for_week(week, username))
    else:
        return num_loss_in_week(week) * WEEKLY_BET

def num_won_in_week(week):
    total_users = session.query(Picks.username)\
                        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
                        .filter(TeamWeek.week == week)\
                        .distinct()\
                        .count()

    return total_users - num_loss_in_week(week)

def num_loss_in_week(week):
    return session.query(Picks.username)\
                        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
                        .filter(TeamWeek.busted == True)\
                        .filter(TeamWeek.week == week)\
                        .distinct()\
                        .count()


def user_lost_in_week(week, username):
    return session.query(Picks.username)\
              .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
                        .filter(Picks.username == username)\
                        .filter(TeamWeek.week == week)\
                        .filter(TeamWeek.busted == True)\
                        .distinct()\
                        .scalar() is not None

def penalty_for_week(week, username):
    return session.query(Picks.username)\
              .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
              .filter(Picks.username == 'Chris Farrell')\
              .filter(TeamWeek.week == 2)\
              .filter(TeamWeek.busted == True)\
              .count() > 1
