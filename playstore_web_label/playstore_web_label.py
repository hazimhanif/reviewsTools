# -*- coding: utf-8 -*-

'''
Created on 16 Dec 2016

@author: Hazim Hanif
'''
import os

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import flask
import pymysql
import dbase_stuff as dbs

global revId
global nameIncoming

app = Flask(__name__)
revId=0
nameIncoming=""


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return main_screen()
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    global nameIncoming
    user=dbs.login(request.form['username'])
    if request.form['password'] == user[1] and request.form['username'] == user[0]:
        session['logged_in'] = True
        nameIncoming=request.form['username']
    else:
        flash('Wrong password!')
    return home()

@app.route('/result', methods=['POST'])
def result():
    addLabel(request.form['sentiment'],request.form['authenticity'],request.form['rating'],nameIncoming)
    dbs.addReviewsCount(nameIncoming)
    dbs.revUnlock(revId)
    return redirect(url_for('main_screen'))

@app.route('/drop')
def drop():
    dbs.setDrop(nameIncoming,revId)
    dbs.revUnlock(revId)
    return redirect(url_for('main_screen'))

@app.route('/main')
def main_screen():
    global revId
    revdrop=dbs.getTotalReviewsDrop(nameIncoming)
    review=dbs.getReview(nameIncoming)
    revId=review[0]
    dbs.revLock(nameIncoming,revId)
    return render_template('main.html',revdrop=revdrop,review=review,nameIncoming=nameIncoming)

def addLabel(sentiment,authenticity,rating,nameIncoming):
    dbs.setLabel(sentiment,authenticity,rating,nameIncoming,revId)

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error_400.html'),400

@app.route("/logout")
def logout():
    dbs.revUnlock(revId)
    session['logged_in'] = False
    return home()
 
def main():
    print("Preparing connection to database...")
    dbs.prepare_Database()
    print("Starting webserver...")
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0")

if __name__ == '__main__':
    main()