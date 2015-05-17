# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, flash
from flask_appconfig import AppConfig

from flask_bootstrap import Bootstrap

from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
import flask


app_title ="Demo App"
brand = "ECT"
page_info = {'app_title':app_title, 'Brand':brand}


import navigation

class page_props ():
    def __init__(self, title, pageType):
	self.title = title
	self.page_type = pageType
	pass    
    
    def run (self):
	page_info['title'] = self.title
	page_info['page_type'] = self.page_type
	return page_info

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    title = "About this site"
    pageType = 'about'
    c_about = page_props(title, pageType)
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
	    a = {"pitch":20, "roll": 0, "heading":23}
	    yield 'data: %s\n\n' % json.dumps(a) 

    '''
    search: flask pushing messages
    https://github.com/jakubroztocil/chat/blob/master/app.py
    http://peter-hoffmann.com/stackoverflow/12236019.html
    '''
    @app.route('/attitude_heading')
    def stream():
        return flask.Response(event_att_head(), mimetype="text/event-stream")

    @app.route('/random_gen')
    def random_gen():
	print "hi"    
	ref_data = ref_data = lat_lon.get_nav_data()
	return jsonify(ref_data)


    @app.route('/', methods=['GET', 'POST'])
    def main_app():
	title = "Bienvenido!!"
	paragraph = [u'']
	
	pageType = 'main_app' 

	page_info['title'] = title
	page_info['page_type'] = pageType
        return render_template("index.html", paragraph=paragraph, pageInfo=page_info)


    return app

if __name__ == '__main__':
    App = create_app()	
    App.debug = True
    App.run(threaded=True)

