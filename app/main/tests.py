import os
import unittest

from datetime import date

from app import app, db, bcrypt
from app.models import Player, Coach, User, Team

"""
Run these tests with the command:
python -m unittest app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_teams():
    t1 = Team(name='Carolina Panthers', wins=500, losses=450)
    p1 = Player(
        name='Cam Newton',
        position='Quarterback',
        team=t1
    )
    c1 = Coach(
        name='Ron Rivera',
        position='Head Coach',
        wins=150,
        losses=100,
        team=t1
    )
    db.session.add(p1)
    db.session.add(c1)

    t2 = Team(name='New York Giants', wins=500, losses=500)
    p2 = Player(name='Eli Manning', position='Quarterback', team=t2)
    c2 = Coach(name='Tom Coughlin', position='Head Coach', wins=200, losses=200)
    db.session.add(p2)
    db.session.add(c2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='test', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the teams show up on the homepage."""
        # Set up
        create_teams()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Carolina Panthers', response_text)
        self.assertIn('New York Giants', response_text)
        self.assertNotIn('test', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Player', response_text)
        self.assertNotIn('Create Coach', response_text)
        self.assertNotIn('Create Team', response_text)

    def test_homepage_logged_in(self):
        """Test that the teams show up on the homepage."""
        # Set up
        create_teams()
        create_user()
        login(self.app, 'test', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('New York Giants', response_text)
        self.assertIn('Carolina Panthers', response_text)
        self.assertIn('test', response_text)
        self.assertIn('Create Player', response_text)
        self.assertIn('Create Team', response_text)
        self.assertIn('Create Coach', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_team_detail_logged_out(self):
        """Test that the team appears on its detail page."""
        # Set up
        create_teams()
        create_user()

        # Make a GET request
        response = self.app.get('/teams/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)

        self.assertIn('Carolina Panthers', response_text)
        self.assertIn('Ron Rivera', response_text)
        self.assertIn('Cam Newton', response_text)

        # Check for things we don't expect
        self.assertNotIn('Create Player', response_text)
        self.assertNotIn('Create Coach', response_text)
        self.assertNotIn('Create Team', response_text)

    def test_team_detail_logged_in(self):
        """Test that the team appears on its detail page."""
        # Set up
        create_teams()
        create_user()
        login(self.app, 'test', 'password')

        # Make a GET request
        response = self.app.get('/teams/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)

        self.assertIn('Ron Rivera', response_text)
        self.assertIn('Carolina Panthers', response_text)

    def test_update_team(self):
        """Test updating a team."""
        # Set up
        create_teams()
        create_user()
        login(self.app, 'test', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Atlanta Falcons',
            'wins': 600,
        }
        self.app.post('/teams/1', data=post_data)

        # Make sure the book was updated as we'd expect
        book = Team.query.get(1)
        self.assertEqual(book.name, 'Atlanta Falcons')
        self.assertEqual(book.wins, 600)
