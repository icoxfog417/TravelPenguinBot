import os.path
import json
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.log import gen_log
from linebot.line import Line
from travel_penguin.env import Environment
from travel_penguin.travel.penguin import Penguin


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/callback", BotHandler)
        ]

        env = Environment()

        settings = dict(
            cookie_secret=env.get_secret_token(),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
            line_keys=env.get_line_keys(),
            proxy=env.get_proxy(),
            google_api_key=env.get_google_api_key(),
            database_url=env.get_database_url()
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

    def post(self):
        penguin = Penguin(self.settings["google_api_key"], self.settings["database_url"])
        history = penguin.db.history()
        self.write({"history": history})


class BotHandler(tornado.web.RequestHandler):

    def post(self):
        debug = self.get_argument("debug", False)
        keys = self.settings["line_keys"] + (self.settings["proxy"],)
        line = Line(*keys)
        status = True
        progress = "begin"
        replies = []

        try:
            penguin = Penguin(self.settings["google_api_key"], self.settings["database_url"])

            body = json.loads(self.request.body.decode("utf-8"))
            progress = "success to load body"

            reqs = line.receive(body)
            if len(reqs) == 0:
                raise Exception("No message is received")
            progress = "success to parse request"

            for r in reqs:
                request_msg = r.content
                resp = request_msg.reply()
                result_type, reply = penguin.ask(request_msg.text)
                replies.append(reply)
                resp.set_location(reply, penguin.place.name, penguin.place.lat, penguin.place.lng)

                if not debug:
                    line.post(resp)
                    progress = "success to send message"

        except Exception as ex:
            gen_log.error(str(ex))
            status = False

        self.write({
            "status": status,
            "replies": replies,
            "progress": progress
        })
