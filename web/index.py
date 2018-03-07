#coding:utf-8
from __future__ import unicode_literals
from flask import Flask, render_template,session,redirect,request
from  . import app
import utils


headers = {'content-type': 'application/json'}
#dashboard页面
@app.route('/')
def index():
    if session.get('author','nologin') == 'nologin':
        return redirect('/login')
    username = session.get('username')
    data_asset = utils.api_action('asset.list',{'where':{'status':0}})
    print data_asset
    print "yes"
    return render_template('index.html',user=username)






