import os.path
import json
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.log import gen_log
from linebot.line import Line
from travel_penguin.env import Environment


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/bot", BotHandler)
        ]

        env = Environment()

        settings = dict(
            cookie_secret=env.get_secret_token(),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            line_keys=env.get_line_keys(),
            google_api_key=env.get_google_api_key()
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class BotHandler(tornado.web.RequestHandler):

    def post(self):
        line = Line(*self.settings["line_keys"])
        try:
            body = json.loads(self.request.body.decode("utf-8"))
            reqs = line.receive(body)
            if len(reqs) == 0:
                raise Exception("No message is received")

            msg = reqs[0].content
            resp = msg.reply()
            resp.set_text(msg.text)
            line.post(resp)

        except Exception as ex:
            gen_log.error(str(ex))
