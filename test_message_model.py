import os 
#OS module in Python provides functions for interacting with the
#operating system. OS comes under Python’s standard utility modules.
#This module provides a portable way of using operating system dependent
#functionality

from unittest import TestCase
from sqlalchemy import exc #sqlalchemy exceptions

from models import db, User, Message, Follows, Likes

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
        """Create test client,add sample data"""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing" , "testing@test.com" , "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res

def test_message_model(self):
    """Does basic model work"""

    m = Message(
        text = "a warble",
        user_id = self.uid
    )

    db.session.add(m)
    db.session.commit()

    #User should have 1 message
    self.assertEqual(len(self.u.messages), 1)
    self.assertEqual(self.u.messages[0].text, "a warble")


def test_message_likes(self):
    m1 = Message(
        text = "a warble",
        user_id = self.uid
    )

    m2 = Message(
        text = "a very interesting warble",
        user_id = self.uid
    )
#line80 syntax error
    u = User.signup("yetanothertest" , "t@email.com" , "password" , None)
    uid=888
    u.id = uid
    db.session.add_all([m1,m2,u])
    db.session.commit()

    u.likes.append(m1)

    db.session.commit()

    l = Likes.query.filter(Likes.user_id == uid).all()
    self.assertEqual(len(l) , 1)
    self.assertEqual(l[0].message_id , m1.id)
