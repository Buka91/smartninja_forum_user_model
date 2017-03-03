#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers.base import BaseHandler
from models.topic import Topic

class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    def post(self):
        current_user = self.request.cookies.get("current-user")
        if not current_user:
            return self.write("Please login before you're allowed to post a topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic(title=title, content=text, author_username = current_user)
        new_topic.put()  # put() saves the object in Datastore

        params = {"topic": new_topic}
        return self.render_template("topic_details.html", params = params)

class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        params = {"topic": topic}
        return self.render_template("topic_details.html", params = params)