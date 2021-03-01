"""Create database models to represent tables."""
from app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Team(db.Model):
    """Team model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    players = db.relationship('Player', back_populates='team')
    coaches = db.relationship('Coach', back_populates='team')
    usersFavoriting = db.relationship('User', back_populates='team')

    def __str__(self):
        return f'{self.name}:\nWin/Loss:{self.wins}/{self.losses}'

    def __repr__(self):
        return f'<Team: {self.name}>'

class Player(db.Model):
    """Player model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)

    # What team this player is on
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', back_populates='players')

    def __str__(self):
        return f'{self.name}:\nPosition:{self.position}'

    def __repr__(self):
        return f'<Player: {self.name}>'

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)

    # What team this player is on
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', back_populates='coaches')

    def __str__(self):
        return f'{self.name}:\nPosition:{self.position}'

    def __repr__(self):
        return f'<Coach: {self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    # What is this users favorite team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', back_populates='usersFavoriting')

    def __str__(self):
        return f'{self.username}: {self.team.name}'

    def __repr__(self):
        return f'<User: {self.username}>'
