import os
import sys
from tornado.options import options, define
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

app_path = os.path.abspath(os.path.join(
    os.path.abspath(__file__), os.pardir))  # /root/zanhu/config..
sys.path.append(os.path.join(app_path, 'zanhu'))  # /root/zanhu/zanhu

define("port", default=6000, type=int, help="run on the given port")

def main():
    tornado.options.parse_command_line()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    http_server = tornado.httpserver.HTTPServer(wsgi_app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

