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

    def setUp(self): #runs before each test case
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

    def test_repr(self):
        """Does this function show user?"""
        u = User(
            id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit(u)
    
    #user should have the following message
    self.assertEqual(repr(u) , '<User #1:testuser, test@test.com>') ###what is repr(u)

    def test_is_followed_by_(self):
        """Does this function show user?"""

        u1 = User(
            id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
        )

        u2 = User(
            id=2,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2",
        )

        

        follow = FollowersFollowee(
            followee_id=1,
            follower_id=2
        )

    
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        db.session.add(follow)
        db.session.commit()

        #user should have the following message
        self.assertEqual(u2.is_followed_by(u1),True)
        self.assertEqual(u2.followers.first(),u1)

