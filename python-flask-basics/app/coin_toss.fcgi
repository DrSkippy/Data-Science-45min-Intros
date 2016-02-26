#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from  coin_toss import app

if __name__ == '__main__':
    # start the WSGI gateway server
    # for nginx, the bindAddress must be an explicit socket location
    # and rw permissions must match the server's
    WSGIServer(app, bindAddress='/opt/twitter/var/coin_toss-fcgi.sock').run()
