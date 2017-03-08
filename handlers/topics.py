#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers.base import BaseHandler, is_local
from models.comment import Comment
from models.topic import Topic
from google.appengine.api import memcache
import time

class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    def post(self):
        current_user = self.request.cookies.get("current-user")
        user_email = self.request.cookies.get("user-email")
        if not current_user:
            return self.write("Please login before you're allowed to post a topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        csrf_token = self.request.get("csrf_token")
        csrf_value = memcache.get(csrf_token)
        if str(csrf_value) != user_email:
            return self.write("You are hecker!")

        new_topic = Topic(title=title, content=text, author_username = current_user)
        new_topic.put()  # put() saves the object in Datastore

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id=new_topic.key.id())

class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query().filter(Comment.topic_id == int(topic_id), Comment.deleted == False).fetch()
        params = {"topic": topic, "comments": comments}
        return self.render_template("topic_details.html", params = params)

    def post(self, topic_id):
        current_user = self.request.cookies.get("current-user")
        user_email = self.request.cookies.get("user-email")
        if not current_user:
            return self.write("Please login before you're allowed to post a topic.")

        # CSRF protection
        csrf_token = self.request.get("csrf_token")
        csrf_value = memcache.get(csrf_token)
        if str(csrf_value) != user_email:
            return self.write("You are hecker!")

        current_topic = Topic.get_by_id(int(topic_id))
        content = self.request.get("get_comment")

        new_comment = Comment(content=content, author_username=current_user, topic_id=int(topic_id),
                      topic_title=current_topic.title)
        new_comment.put()

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id=int(topic_id))