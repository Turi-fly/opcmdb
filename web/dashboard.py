#encoding:utf-8
#from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, render_template,session,redirect,request
from  . import app
import requests,json
import utils

headers = {'content-type': 'application/json'}
#deshboard页面
@app.route('/')
def index():
 if session.get('author','nologin') == 'nologin':
     return redirect('/login')
 username = session.get('username')
 yn_server_machen = utils.api_action('server.machen',{'where':{'idc_id':13,'status':0}})
 yn_server_machen = json.loads(yn_server_machen).get('result', {})
 server_machen = [yn_server_machen[0]['count(*)']]
 server_model = utils.api_action('server.model', {'where': {'status': 0}})
 server_model = json.loads(server_model).get('result', {})
 category = [item.encode("utf-8") for item in server_model.keys()]
 server_spec = utils.api_action('server.specific', {'where': {'status': 0}})
 server_spec = json.loads(server_spec).get('result', {})
 specification = [item.encode("utf-8") for item in server_spec.keys()]
 server_cabinet = utils.api_action('server.cabinet_machen', {'where':{'status': 0}})
 server_cabinet = json.loads(server_cabinet).get('result', {})
 cabinet = [item.encode("utf-8") for item in server_cabinet.keys()]
 return render_template('index.html',user=username,server_machen=server_machen,\
                                    category=category,server_model=server_model, \
                                    spec=specification,server_spec=server_spec,\
                                    cabinet=cabinet,server_cabinet=server_cabinet)


@app.route('/index1')
def index1():
 if session.get('author','nologin') == 'nologin':
     return redirect('/login')
 username = session.get('username')
 yn_server_machen = utils.api_action('server.machen',{'where':{'idc_id':13,'status':0}})
 yn_server_machen = json.loads(yn_server_machen).get('result', {})
 server_machen = [yn_server_machen[0]['count(*)']]
 return render_template('index1.html',user=username,server=server_machen)


@app.route('/index2')
def index2():
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    username = session.get('username')
    server_model = utils.api_action('server.model',{'where':{'status':0}})
    server_model = json.loads(server_model).get('result', {})
    category = [ item.encode("utf-8") for item in server_model.keys() ]
    server_model_yn = utils.api_action('server.model',{'where':{'idc_id':13,'status':0}})
    server_model_yn = json.loads(server_model_yn).get('result', {})
    #server_model_sb = utils.api_action('server.model',{'where':{'idc_id':15,'status':0}})
    #server_model_sb = json.loads(server_model_sb).get('result', {})
    model_list = app.config['cursor'].get_results('model', ['id', 'model'])
    model_list = dict([item.values() for item in model_list])
    model_dict = {}
    for item in model_list:
        model_dict[item.encode("utf-8")] = int(model_list[item])
    return render_template('index2.html', user=username,category=category,\
                           server_model_yn=server_model_yn,model_dict=model_dict)


@app.route('/index3')
def index3():
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    username = session.get('username')
    server_spec = utils.api_action('server.specific',{'where':{'status':0}})
    server_spec = json.loads(server_spec).get('result',{})
    specification = [ item.encode("utf-8") for item in server_spec.keys() ]
    server_spec_yn = utils.api_action('server.specific',{'where':{'status':0,'idc_id':'13'}})
    server_spec_yn = json.loads(server_spec_yn).get('result',{})
    #server_spec_sb = utils.api_action('server.specific',{'where':{'status':0,'idc_id':'15'}})
    #server_spec_sb = json.loads(server_spec_sb).get('result',{})
    spec_list = app.config['cursor'].get_results('spec', ['spec', 'id'])
    spec_list = dict([item.values() for item in spec_list])
    spec_dict = {}
    for item in spec_list:
        spec_dict[item.encode("utf-8")] = int(spec_list[item])
    return render_template('index3.html', user=username,spec=specification,server_spec_yn=server_spec_yn,\
                          spec_dict=spec_dict)


@app.route('/index4')
def index4():
    if session.get('author', 'nologin') == 'nologin':
        return redirect('/login')
    username = session.get('username')
    server_cabinet = utils.api_action('server.cabinet_machen', {'where': {'status': 0}})
    server_cabinet = json.loads(server_cabinet).get('result', {})
    cabinet = [item.encode("utf-8") for item in server_cabinet.keys()]
    cabinet_list = app.config['cursor'].get_results('cabinet', ['cabinet_num', 'id'])
    cabinet_list = dict([item.values() for item in cabinet_list])
    cabinet_dict = {}
    for item in cabinet_list:
        cabinet_dict[item.encode("utf-8")] = int(cabinet_list[item])
    return render_template('index4.html', user=username,cabinet=cabinet,server_cabinet=server_cabinet,cabinet_dict=cabinet_dict)


@app.route('/user/<htmlname>')
def user(htmlname):
 if session.get('author','nologin') == 'nologin':
     return redirect('/login')
     utils.write_log('web').info("info")
 return render_template(htmlname +'.html',user=session.get('username'))


@app.route('/project/<htmlname>')
def project(htmlname):
 if session.get('author','nologin') == 'nologin':
     return redirect('/login')
 return render_template(htmlname +'.html',user=session.get('username'))


@app.route('/cmdb/<htmlname>')
def cmdb(htmlname):
 if session.get('author','nologin') == 'nologin':
     return redirect('/login')
 return render_template(htmlname +'.html',user=session.get('username'))


@app.errorhandler(404)    #系统自带的装饰器，遇到404回自动返回制定的404页面
def not_found(e):
 return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html')
