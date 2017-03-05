#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from handlers.base import BaseHandler
from models.users import User

class RegisterHandler(BaseHandler):
    def get(self):
        return self.render_template("register.html")


class LoginHandler(BaseHandler):
    def get(self):
        if self.request.cookies.get("user-email") and self.request.cookies.get("current-user"):
            # user is logged in
            self.response.delete_cookie(key = "user-email")
            self.response.delete_cookie(key = "current-user")
        return self.render_template("login.html")

    def post(self):
        username = self.request.get("username")
        email = self.request.get("email")
        password = hashlib.sha512(b"" + self.request.get("password")).hexdigest()
        rep_password = hashlib.sha512(b"" + self.request.get("confirm_password")).hexdigest()

        if password != rep_password:
            return self.write("Confirm password and password are not the same!")

        if "@" not in email:
            return self.write("Invalid email address.")

        exist_user = User.query().filter(User.username == username).fetch()
        exist_email = User.query().filter(User.email == email).fetch()
        exist_pass = User.query().filter(User.password == password).fetch()

        if len(exist_user) > 0 or len(exist_email) > 0 or len(exist_pass) > 0:
            return self.write("User with this username, email or password already exist.")

        user = User(username = username, email = email, password = password)
        user.put()

        return self.redirect_to("login")