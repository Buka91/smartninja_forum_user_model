#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def get_or_create(cls, email):
        user = User.query(User.email == email).get()  # check if user already exists in the database

        if not user:
            # if user does not exist yet, create a new one
            user = User(email=email)
            user.put()


        return user