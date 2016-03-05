#!/usr/bin/env python
import datetime
import json
import logging
import tornado.websocket
import uuid
 
from tornado import gen
from django.utils.timezone import utc
from modules.message_buffer import MessageBuffer

message_buffers = dict()
 
class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado')

class MessageNewHandler(tornado.web.RequestHandler):
    def post(self, lobby_id):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
            "user_id": self.get_argument("user_id"),
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        if (message["body"] == None or message["body"] == ""):
            self.write("")
            return
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        if (not message_buffers.has_key(lobby_id)):
            logging.info("Creating buffer for lobby " + lobby_id)
            message_buffers[lobby_id] = MessageBuffer()
        logging.info("New message in lobby " + lobby_id)
        message_buffers[lobby_id].new_messages([message])


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self, lobby_id):
        cursor = self.get_argument("cursor", None)
        self.lobby_id = lobby_id
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        if (not message_buffers.has_key(self.lobby_id)):
            logging.info("Creating buffer for lobby " + self.lobby_id)
            message_buffers[self.lobby_id] = MessageBuffer()
        logging.info("Listening on lobby " + self.lobby_id)
        self.future = message_buffers[self.lobby_id].wait_for_messages(cursor=cursor)
        messages = yield self.future
        logging.info("Recieved message")
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        if (message_buffers.has_key(self.lobby_id)):
            message_buffers[self.lobby_id].cancel_wait(self.future)

class MessageCacheHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self, lobby_id):
        if (message_buffers.has_key(lobby_id)):
            self.write(dict(messages=message_buffers[lobby_id].cache))
        else:
            self.write(dict(messages=[]))