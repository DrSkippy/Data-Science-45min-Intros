#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from  coin_toss import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/opt/twitter/var/coin_toss-fcgi.sock').run()
