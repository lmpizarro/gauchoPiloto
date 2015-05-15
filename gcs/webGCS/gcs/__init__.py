# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify


app_title ="webGCS"
brand = "ECT"
page_info = {'app_title':app_title, 'Brand':brand}


# straight from the wtforms docs:
class LoginForm(Form):
    username = TextField('username', [validators.required()])
    password = TextField('password', [validators.required()])
    submit_button = SubmitField('Submit Form')

class ContactForm(Form):
    email = TextField('email', [validators.required()])
    name = TextField('name', [validators.required()])
    phone = TextField('phone', [validators.required()])
    message = TextField('message', [validators.required()])
    submit_button = SubmitField('Submit Form')

class page_props ():
    def __init__(self, title, pageType):
	self.title = title
	self.page_type = pageType
	pass    
    
    def run (self):
	page_info['title'] = self.title
	page_info['page_type'] = self.page_type
	return page_info

import navigation

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    title = "About"
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

    @app.route('/random_gen')
    def random_gen():
	print "hi"    
	ref_data = lat_lon.get_nav_data()
	return jsonify(ref_data)

    @app.route('/about')
    def about():
        paragraph = ["blah blah blah memememememmeme blah blah memememe"]

        return render_template("about.html", paragraph=paragraph, pageInfo= c_about.run())

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():

        title = "Logout"
        paragraph = ["Gracias por visitarnos"]

        pageType = 'logout'

	page_info['title'] = title
	page_info['page_type'] = pageType

	session['logged_in'] = False
        form = LoginForm()

        if session['logged_in'] != True:
             return redirect(url_for('index'))
        return render_template("main_app.html", paragraph=paragraph, pageInfo=page_info)

    @app.route('/contact')
    def contact():

        title = u'Contacto'
        paragraph = [u'Acá va un formulario de contacto']

        pageType = 'contact'

	page_info['title'] = title
	page_info['page_type'] = pageType
        form = ContactForm()
	try:    
            return render_template("contact.html", paragraph=paragraph, pageInfo=page_info, form=form)
        except Exception, e:
	    return str(e)




    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index', methods=['GET', 'POST'])
    def index():
	title = "Login"
	paragraph = [u'Por favor ingrese a la aplicación!']
	pageType = 'index' 

	page_info['title'] = title
	page_info['page_type'] = pageType

        error = None
        if request.method == 'POST':
	        if request.form['username'] != app.config['USERNAME']:
		            error = 'Invalid username'
	        elif request.form['password'] != app.config['PASSWORD']:
	                    error = 'Invalid password'
	        else:
	            session['logged_in'] = True
	            return redirect(url_for('main_app'))

        form = LoginForm()
        return render_template("index.html", paragraph=paragraph, pageInfo=page_info, form=form)

    @app.route('/main_app', methods=['GET', 'POST'])
    def main_app():
	title = "Bienvenido!!"
	paragraph = [u'']
	
	pageType = 'main_app' 

	page_info['title'] = title
	page_info['page_type'] = pageType
        if session['logged_in'] != True:
             return redirect(url_for('index'))
        return render_template("main_app.html", paragraph=paragraph, pageInfo=page_info)


    return app

if __name__ == '__main__':
    create_app().run(debug=True)
