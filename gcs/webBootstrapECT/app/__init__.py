# -*- coding: utf-8 -*-
#from __future__ import absolute_import

from flask import Flask
from flask import render_template
from flask_appconfig import AppConfig

from flask_bootstrap import Bootstrap

from flask import url_for
from flask import jsonify
import flask

import random
import navigation

import commands

import redis

redis_server = redis.Redis("127.0.0.1")
redis_subscriber = redis_server.pubsub()
redis_subscriber.subscribe("udp_read15550")




def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    lat_lon = navigation.nav_data()

    # initialization 
    app.config['USERNAME'] = 'admin@pepe.com'
    app.config['PASSWORD'] = 'default'

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    import time
    import json

    def event_att_head():
        while True:
	    time.sleep(1)
	    print "event_stream"
	    a = {"pitch":0 + random.gauss(0,1), "roll": 0 + random.gauss(0,1), "heading":23 + + random.gauss(0,10)}
	    yield 'data: %s\n\n' % json.dumps(a) 

    def event_udp_read():
        for message in redis_subscriber.listen():
            print message
            yield 'data: %s\n\n' % json.dumps ({'udp_mess': message['data']})

    '''
    search: flask pushing messages
    https://github.com/jakubroztocil/chat/blob/master/app.py
    http://peter-hoffmann.com/stackoverflow/12236019.html
    '''
    @app.route('/attitude_heading')
    def stream():
        return flask.Response(event_att_head(), mimetype="text/event-stream")

    @app.route('/udp_read')
    def stream_udp():
        return flask.Response(event_udp_read(), mimetype="text/event-stream")


    @app.route('/_gps_data')
    def gps_data():
	print "hi"    
	ref_data = lat_lon.get_nav_data()
	return jsonify(ref_data)

    @app.route('/')
    def main_app():
        return render_template("index.html")

    return app
