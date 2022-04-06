"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

#OS module in Python provides functions for interacting with the
#operating system. OS comes under Python’s standard utility modules.
#This module provides a portable way of using operating system dependent
#functionality.

import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test" #modify the environmet variable


#os.environ in Python is a mapping object that represents the user’s environmental 
#variables. It returns a dictionary having user’s environmental variable as key and 
#their values as value.os.environ behaves like a python dictionary, so all the common
#dictionary operations like get and set can be performed. 

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)