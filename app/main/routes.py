"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import Player, Team, Coach, User
from app.main.forms import CoachForm, TeamForm, PlayerForm
from app import bcrypt

# Import app and db from events_app package so that we can run app
from app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_users = User.query.all()
    return render_template('home.html', all_users=all_users)

@main.route('/teams')
def all_teams():
    all_teams = Team.query.all()
    return render_template('all_teams.html', teams=all_teams)

@main.route('/create_team', methods=['GET','POST'])
@login_required
def create_team():
    form = TeamForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        print('submitting...')
        new_team = Team(
            name=form.name.data,
            wins=form.wins.data,
            losses=form.losses.data
        )
        db.session.add(new_team)
        db.session.commit()

        flash('New team was created successfully.')
        return redirect(url_for('main.team_detail', team_id=new_team.id))
    return render_template('create_team.html', form=form)


@main.route('/teams/<team_id>', methods=['GET', 'POST'])
def team_detail(team_id):
    team = Team.query.get(team_id)
    form = TeamForm(obj=team)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        team.name = form.name.data
        team.wins = form.wins.data
        team.losses = form.losses.data
        team.coach = form.coach.data

        db.session.commit()

        flash('Team was updated successfully.')
        return redirect(url_for('main.team_detail', team_id=team_id))

    return render_template('team_detail.html', team=team, form=form)

@main.route('/create_coach', methods=['GET','POST'])
@login_required
def create_coach():
    form = CoachForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_coach = Coach(
            name=form.name.data,
            position=form.position.data,
            wins=form.wins.data,
            losses=form.losses.data,
        )
        db.session.add(new_coach)
        db.session.commit()

        flash('New coach was created successfully.')
        return redirect(url_for('main.coach_detail', coach_id=new_coach.id))
    return render_template('create_coach.html', form=form)

@main.route('/coaches')
def all_coaches():
    all_coaches = Coach.query.all()
    return render_template('all_coaches.html', coaches=all_coaches)


@main.route('/coaches/<coach_id>', methods=['GET', 'POST'])
def coach_detail(coach_id):
    coach = Coach.query.get(coach_id)
    form = CoachForm(obj=coach)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        coach.name = form.name.data
        coach.wins = form.wins.data
        coach.losses = form.losses.data
        coach.position = form.position.data
        coach.team = form.team.data

        db.session.commit()

        flash('Coach was updated successfully.')
        return redirect(url_for('main.coach_detail', coach_id=coach_id))

    return render_template('coach_detail.html', coach=coach, form=form)


@main.route('/create_player', methods=['GET','POST'])
@login_required
def create_player():
    form = PlayerForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_player = Player(
            name=form.name.data,
            position=form.position.data,
            team=form.team.data
        )
        db.session.add(new_player)
        db.session.commit()

        flash('New player was created successfully.')
        return redirect(url_for('main.player_detail', player_id=new_player.id))
    return render_template('create_player.html', form=form)

@main.route('/players')
def all_players():
    all_players = Player.query.all()
    return render_template('all_players.html', players=all_players)

@main.route('/players/<player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    player = Player.query.get(player_id)
    form = PlayerForm(obj=player)

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        player.name = form.name.data
        player.wins = form.wins.data
        player.losses = form.losses.data
        player.position = form.position.data
        player.team = form.team.data

        db.session.commit()

        flash('Player was updated successfully.')
        return redirect(url_for('main.player_detail', player_id=player_id))

    return render_template('player_detail.html', player=player, form=form)
