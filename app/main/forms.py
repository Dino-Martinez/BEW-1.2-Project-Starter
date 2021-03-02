from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Player, Team, Coach, User

class TeamForm(FlaskForm):
    """Form to create a team."""
    name = StringField('Team Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    wins = IntegerField('All Time Wins', validators=[DataRequired()])
    losses = IntegerField('All Time Losses', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PlayerForm(FlaskForm):
    """Form to create a player."""
    name = StringField('Player Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    position = StringField('Player Position',
        validators=[DataRequired(), Length(min=3, max=80)])
    team = QuerySelectField('Team',
        query_factory=lambda: Team.query, allow_blank=False)
    submit = SubmitField('Submit')

class CoachForm(FlaskForm):
    """Form to create a coach."""
    name = StringField('Coach Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    position = StringField('Coach Position',
        validators=[DataRequired(), Length(min=3, max=80)])
    wins = IntegerField('All Time Wins', validators=[DataRequired()])
    losses = IntegerField('All Time Losses', validators=[DataRequired()])
    team = QuerySelectField('Team',
        query_factory=lambda: Team.query, allow_blank=False)
    submit = SubmitField('Submit')
