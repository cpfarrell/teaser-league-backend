13# -*- coding: utf-8 -*-

import datetime
import hashlib
import time

from flask import Flask
from flask import jsonify
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import not_
from sqlalchemy import or_
from sqlalchemy import exists

from teaser_league_backend.constants import MAIN_TEASER_LEAGUE_2018_ID
from teaser_league_backend.logic.base import Base
from teaser_league_backend.logic.team_week import TeamWeek
from teaser_league_backend.logic.picks import Picks
from teaser_league_backend.logic.users import Users
from teaser_league_backend.logic.league_users import LeagueUsers
from teaser_league_backend.logic.leagues import Leagues


app = Flask(__name__)

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

WEEKLY_BET = 15

def authenticate_user(username, password):
    login_success = session.query(Users).filter(Users.username==username).filter(Users.password==password).count() == 1
    print('Login was {}'.format('successful' if login_success else 'unsuccessful'))
    return login_success

def generate_user_token(username):
    return hashlib.md5(username.encode('utf-8')).hexdigest()


@app.route('/login', methods = ['POST'])
def login():
    auth_json = request.get_json()
    print("Auth Req: " + str(auth_json))
    if authenticate_user(auth_json.get('username'), auth_json.get('password')):
        ret = {'status': 'success', 'id_token': generate_user_token(auth_json['username'])}
        print(ret)
        return jsonify(ret)

    # Failed auth.
    ret = {'status': 'fail', 'ERROR': 'sad face'};
    return jsonify(ret);

@app.route('/users/<league_id>')
def users(league_id=None):
    result = session.query(LeagueUsers.username).filter(LeagueUsers.teaser_league_id==league_id).all()
    usernames = [username for (username,) in result]
    return jsonify(usernames)

@app.route('/users')
def all_users(league_id=None):
    result = session.query(Users.username).all()
    usernames = [username for (username,) in result]
    return jsonify(usernames)

@app.route('/leagues/<user_id>')
def leagues_per_user(user_id):
    #result = session.query(LeagueUsers.username).filter(LeagueUsers.teaser_league_id==league_id).all()
    result = session.query(LeagueUsers.teaser_league_id)\
            .join(Leagues, Leagues.teaser_league_id==LeagueUsers.teaser_league_id)\
            .filter(LeagueUsers.username==user_id)\
            .all()
    leagues = [league for (league,) in result]
    return jsonify(leagues)

@app.route('/leaderboard/<league_id>/')
def leaderboard(league_id):
    start = time.time()
    rankings = _leaderboard(league_id)
    print("Time to get leaderboard:  {} seconds".format(time.time() - start))
    return jsonify(rankings)

def _leaderboard(league_id):
    scores = []
    for username, in session.query(LeagueUsers.username).filter(LeagueUsers.teaser_league_id==league_id):
        total_points = 0
        for week in weeks_in_league(league_id):
            total_points += get_won_loss_for_week(week, username, league_id)
        scores.append({'username': username, 'points': total_points})
    return sorted(scores, key=lambda k: k['points'], reverse=True)

def weeks_in_league(league_id):
    sports_league = session.query(Leagues.sports_league).filter(Leagues.teaser_league_id==league_id).distinct().one()[0]
    sports_year = session.query(Leagues.sports_year).filter(Leagues.teaser_league_id==league_id).distinct().one()[0]
    for week, in session.query(TeamWeek.week).filter(and_(TeamWeek.year==sports_year, TeamWeek.sports_league==sports_league)).distinct().order_by(TeamWeek.week):
        yield week

@app.route('/list_of_weeks/<league_id>/<username>/')
def list_of_weeks(username, league_id):
    weeks = []
    for week, in session.query(TeamWeek.week)\
                        .join(Leagues, Leagues.sports_league==TeamWeek.sports_league)\
                        .filter(Leagues.teaser_league_id==league_id)\
                        .distinct()\
                        .order_by(TeamWeek.week):
        weeks.append({'week': week, 'points': get_won_loss_for_week(week, username, league_id)})
    return jsonify(weeks)

@app.route('/weekly_picks/<league_id>')
def get_num_weeks(league_id):
    weeks = []
    # select team_week.sports_league, COUNT(distinct team_week.week)  from team_week JOIN leagues ON team_week.sports_league = leagues.sports_league AND team_week.year=leagues.sports_year GROUP BY 1;
    num_weeks = session.query(TeamWeek.week)\
                        .join(Leagues, and_(Leagues.sports_league == TeamWeek.sports_league, Leagues.sports_year == TeamWeek.year))\
                        .filter(Leagues.teaser_league_id==league_id)\
                        .distinct()\
                        .count()
        #weeks.append({'week': week, 'points': get_won_loss_for_week(week, username, league_id)})
    return jsonify({'num_weeks': num_weeks})

@app.route('/weekly_picks/<league_id>/<week>/<username>/')
def week_breakdown(week, username, league_id):
    start = time.time()
    response = {}
    teams = []
    for result in session.query(TeamWeek, Picks)\
                        .outerjoin(Picks, and_(Picks.team==TeamWeek.team, Picks.week==TeamWeek.week, Picks.username==username))\
                        .join(Leagues, and_(Leagues.sports_league == TeamWeek.sports_league, Leagues.sports_year == TeamWeek.year))\
                        .filter(Leagues.teaser_league_id==league_id)\
                        .filter(TeamWeek.week==week)\
                        .order_by(TeamWeek.game_time, TeamWeek.game_id)\
                        .all():
        teams.append(
            {
                'team': result.TeamWeek.team,
                'game_time': str(result.TeamWeek.game_time),
                'spread': result.TeamWeek.adjusted_spread,
                'pick': '' if (result.Picks is None or not pick_can_be_shown(result.TeamWeek.game_time)) else 'X',
                'score': result.TeamWeek.score,
                'busted': get_busted_string(result.TeamWeek),
                'locked': result.TeamWeek.game_time < datetime.datetime.now(),
                'picks': num_picked_team_week(result.TeamWeek),
                'users_who_picked': users_who_picked_team_in_week(result.TeamWeek),
            }
        )
    response['teams'] = teams
    #rankings = _leaderboard(league_id)
    #response['losers'] = add_rank_to_user_list(losers_for_week(week, only_final=True), rankings)
    #response['losers_if_scores_hold'] = add_rank_to_user_list(losers_for_week(week, only_final=False), rankings)
    #response['penalties'] = add_rank_to_user_list(penalties_for_week(week, only_final=True, num_losses=2), rankings)
    #response['winners'] = add_rank_to_user_list(winners_for_week(week), rankings)

    response['losers'] = losers_for_week(week, league_id, only_final=True)
    response['losers_if_scores_hold'] = losers_for_week(week, league_id, only_final=False)
    response['penalties'] = penalties_for_week(week, league_id, only_final=True, num_losses=2)
    response['winners'] = winners_for_week(week, league_id)

    print("Time to get weekly picks:  {} seconds".format(time.time() - start))
    return jsonify(response)

def add_rank_to_user_list(users, rankings):
    users_with_rank = []
    for user in users:
        for rank, info in enumerate(rankings):
            if info['username'] == user:
                users_with_rank.append({'username': user, 'points': info['points'], 'rank': rank + 1})
    return users_with_rank

def pick_can_be_shown(game_time):
    (
        # Game is happening at least with the next 2 days.
        game_time > datetime.datetime.now() + datetime.timedelta(days=365-2) and (
            # Game is on Thursday so relese bets at 5pm.
            (datetime.datetime.now().weekday() == 3 and datetime.datetime.now().hour >= 17)
            # Game is on sunday so close betting at 1 pm.
            (datetime.datetime.now().weekday() == 6 and datetime.datetime.now().hour >= 13)
        )
    )

# This should be a check against active sessions on a backend, looking for timeouts.
def pick_is_for_current_user_or_user_is_admin(username, id_token):
    """ Doesn't check for admin mode yet! """
    print("Auth Check: (%s):" % username, generate_user_token(username), id_token)
    print ("Username {}, Expected: {}, passed in token: {}".format(username, generate_user_token(username), id_token))
    return generate_user_token(username) == id_token

@app.route('/make_picks/<week>/<username>', methods = ['POST'])
def make_picks(week, username):
    data = request.get_json()
    print(data)

    if not pick_is_for_current_user_or_user_is_admin(username, data['id_token']):
        print("pick auth failed for request:")
        print(data)
        return jsonify({'success': False})
    print("auth allowed")

    session.query(Picks).filter(Picks.username==username).filter(Picks.week==week).delete()
    teams = data['teams']
    for team in teams:
        session.add(Picks(username=username, team=team, week=week))
    session.commit()
    return jsonify({'success': True})

def get_won_loss_for_week(week, username, league_id):
    if user_lost_in_week(week, username, league_id):
        basic_loss = num_won_in_week(league_id, week) * WEEKLY_BET * -1
        return basic_loss - (20 * was_in_penalty_for_week(week, username, league_id))
    else:
        return len(losers_for_week(week, league_id)) * WEEKLY_BET

def num_won_in_week(league_id, week):
    total_users = session.query(LeagueUsers).filter(LeagueUsers.teaser_league_id == league_id).count()
    return total_users - num_loss_in_week(week)

def num_loss_in_week(week):
    return session.query(Picks.username)\
                        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
                        .filter(busted(TeamWeek))\
                        .filter(TeamWeek.week == week)\
                        .distinct()\
                        .count()


def user_lost_in_week(week, username, league_id):
    return session.query(Picks.username)\
              .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
                        .filter(Picks.username == username)\
                        .filter(Picks.teaser_league_id == league_id)\
                        .filter(TeamWeek.week == week)\
                        .filter(busted(TeamWeek))\
                        .filter(TeamWeek.game_final)\
                        .distinct()\
                        .scalar() is not None

def was_in_penalty_for_week(week, username, league_id):
    return session.query(Picks.username)\
              .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
              .filter(Picks.username == username)\
              .filter(Picks.teaser_league_id == league_id)\
              .filter(TeamWeek.week == week)\
              .filter(busted(TeamWeek))\
              .count() > 1

def users_who_picked_team_in_week(team_week):
    return [user[0] for user in session.query(Picks.username).filter(
        and_(
            and_(Picks.week==team_week.week, Picks.team==team_week.team),
            pick_can_be_shown(team_week.game_time)
            ),
        )
    ]

def num_picked_team_week(team_week):
    return  len(users_who_picked_team_in_week(team_week))

def get_busted_string(team_week):
    relative_score = score_relative_to_adjusted_spread(team_week)
    if relative_score is None:
        return ''
    elif relative_score <= 0 and team_week.game_final:
        return 'Busted'
    elif relative_score <= 0 and not team_week.game_final and datetime.datetime.now() > team_week.game_time:
        return 'Busting'
    elif relative_score <= 7 and not team_week.game_final and datetime.datetime.now() > team_week.game_time:
        return "Close"
    elif relative_score > 0 and team_week.game_final:
        return "√"
    else:
        return ''

def score_relative_to_adjusted_spread(team_week):
    # Score difference plus adjusted spread.
    # So negative means not covering, positive is covering, and zero is push.
    # Returns None if game has not started
    if team_week.score is None or team_week.opponent_score is None:
        return None
    else:
        return (team_week.score - team_week.opponent_score) + team_week.adjusted_spread

def busted(team_week):
    """Calculates whether the team is busting, whether game is final or not."""
    relative_score = score_relative_to_adjusted_spread(team_week)
    return relative_score is not None and relative_score <= 0

def losers_for_week(week, league_id, only_final=True):
    return penalties_for_week(week, league_id, only_final=only_final, num_losses=1)

def penalties_for_week(week, league_id, only_final=True, num_losses=0):
    return [loser.username for loser in session.query(Picks.username)\
        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
        .join(Leagues, and_(and_(Picks.teaser_league_id==Leagues.teaser_league_id, Leagues.sports_league==TeamWeek.sports_league), Leagues.sports_year==TeamWeek.year))\
        .filter(Picks.teaser_league_id==league_id)\
        .filter(TeamWeek.week == week)\
        .filter(busted(TeamWeek))\
        .filter(or_(TeamWeek.game_final, not only_final))
        .group_by(Picks.username)\
        .having(func.count() >= num_losses)\
        .all()]

def winners_for_week(week, league_id, picks_needed_to_win=4):
    return [winner.username for winner in session.query(Picks.username)\
        .join(TeamWeek, and_(Picks.week==TeamWeek.week, Picks.team==TeamWeek.team))\
        .filter(Picks.teaser_league_id==league_id)\
        .filter(TeamWeek.week == week)\
        .filter(not_(busted(TeamWeek)))\
        .filter(TeamWeek.game_final)
        .group_by(Picks.username)\
        .having(func.count() == picks_needed_to_win)\
        .all()]
