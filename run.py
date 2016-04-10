import os
import tornado
import tornado.ioloop
from travel_penguin.server import Application

if __name__ == "__main__":
    app = Application()
    app.listen(int(os.environ.get("PORT", 8080)))
    tornado.ioloop.IOLoop.current().start()
