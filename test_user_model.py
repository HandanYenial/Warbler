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
from sqlalchemy import exc #sqlalchemy exceptions

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
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


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


#########################################################################
#############FollowingTests##########################################

    def test_user_follows(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(len(self.u2.following) , 0)
        self.assertEqual(len(self.u2.followers) , 1)
        self.assertEqual(len(self.u1.followers) , 0)
        self.assertEqual(len(self.u1.following) , 1)

        self.assertEqual(self.u2.followers[0].id, self.u1.id)
        self.assertEqual(self.u1.following[0].id, self.u2.id)
    
    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u1.is_following(self.u1))

    def test_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    ####################################
    ###########Sign-up tests#############

    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "testtest@test.com", "password", None)
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username , "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")

        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com" , "password" , None)
        uid = 123456789
        invalid.id = uid
        
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    
    def test_invalid_email_signup(self):
        invalid = User.signup("testtest" , None , "password" , None)
        uid = 123789
        invalid.id = uid

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest" , "email@email.com" , "" , None)

######################################################################
##########Authentication Tests########################################

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username , "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id , self.uid1)

    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username , "badpassword"))



  