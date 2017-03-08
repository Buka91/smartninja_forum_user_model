#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import jinja2
import os
import hashlib
from models.topic import Topic
from models.users import User
from google.appengine.api import memcache
import uuid

def is_local():
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        cookie_law = self.request.cookies.get("ninja-cookie")
        if cookie_law:
            params["cookies"] = True

        user_email = self.request.cookies.get("user-email")
        if user_email:
            params["user_email"] = user_email
            # CSRF protection
            csrf_token = str(uuid.uuid4())
            memcache.add(key = csrf_token, value = user_email, time = 600)
            params["csrf_token"] = csrf_token

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == False).fetch()
        #user_email = self.request.cookies.get("user-email")
        #if user_email:
        #    params = {"topics": topics, "user_email": user_email}
        #    return self.render_template("main.html", params = params)
        #else:
        params = {"topics": topics}
        return self.render_template("main.html", params = params)

    def post(self):
        username = self.request.get("username")
        password = hashlib.sha512(b"" + self.request.get("password")).hexdigest()

        users = User.query().filter(User.username == username, User.password == password).fetch()

        if len(users) == 1:
            topics = Topic.query(Topic.deleted == False).fetch()
            params = {"user_email": users[0].email, "topics": topics}
            self.response.set_cookie(key="current-user", value=username)
            self.response.set_cookie(key="user-email", value=users[0].email)
            return self.render_template("main.html", params = params)
        else:
            return self.write("Username or password are incorrect.")


class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")


class CookieAlertHandler(BaseHandler):
    def post(self):
        self.response.set_cookie(key="ninja-cookie", value="accepted")
        return self.redirect_to("main-page")