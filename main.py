#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from handlers.base import MainHandler, CookieAlertHandler, AboutHandler
from handlers.topics import TopicAdd, TopicDetails
from handlers.login import RegisterHandler, LoginHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set_cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/register', RegisterHandler)
], debug=True)
