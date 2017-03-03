#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_username = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True) # čas ob ustvarjanju
    updated = ndb.DateTimeProperty(auto_now=True) # čas, ko se topic posodablja
    deleted = ndb.BooleanProperty(default=False)