from colombia import create_app

import sys

app = create_app()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--gevent":
        from gevent import monkey; monkey.patch_all()
        from gevent.wsgi import WSGIServer
        server = WSGIServer(("0",5000), application=app)
        server.serve_forever()
    else:
        app.run(port=8080)
