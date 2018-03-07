#!/bin/env python
# -*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os, os.path
import time,json
import base64
import hashlib
import traceback
import smtplib
from email.mime.text import MIMEText
from web.email_config import SMTP_SERVER_HOST,SMTP_SERVER_PORT,SMTP_PWD,SMTP_USER
import ConfigParser
import logging,logging.config
import requests
from email.header import Header
from datetime import date,datetime
import  re
from web import app

work_dir = os.path.dirname(os.path.realpath(__file__))
def get_config(section=''):
    config = ConfigParser.ConfigParser()
    service_conf= os.path.join(work_dir, 'conf/service.conf')
    config.read(service_conf)

    conf_items = dict(config.items('common')) if config.has_section('common') else {}
    if section and config.has_section(section):
       conf_items.update(config.items(section))
    return conf_items

def write_log(loggername):
    log_conf= os.path.join(work_dir, 'conf/logger.conf')
    logging.config.fileConfig(log_conf)
    logger = logging.getLogger(loggername)
    return logger

def get_validate(username, uid, role, fix_pwd):
    t = int(time.time())
    return base64.b64encode('%s|%s|%s|%s|%s' % (username, t, uid, role, fix_pwd)).strip()

def validate(key, fix_pwd):
    t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    if len(x) != 5:
        write_log('api').warning("token参数数量不足")
        return json.dumps({'code':1,'errmsg':'token参数不足'})
    if t > int(x[1]) + 2*60*60:
        write_log('api').warning("登录已经过期")
        return json.dumps({'code':1,'errmsg':'登录已过期'})
    if fix_pwd == x[4]:
        write_log('api').info("api认证通过")
        return json.dumps({'code':0,'username':x[0],'uid':x[2],'r_id':x[3]})
    else:
        write_log('api').warning("密码不正确")
        return json.dumps({'code':1,'errmsg':'密码不正确'})
def check_name(name):
    if isinstance(name, str) or isinstance(name, unicode):
        return name.isalnum() and len(name) >= 2
    else:
        return False



#api接口函数
def api_action(methods="",params={}):
    headers = {'content-type':'application/json'}
    url = "http://127.0.0.1:1000/api"
    data = {
        'jsonrpc': '2.0',
        'method': methods,
        'id': '1',
        'params': params

    }
    r = requests.post(url,headers=headers,data=json.dumps(data))
    return r.json().get('result')



#转换时间格式的工具函数
def default(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    return None



#检查ip的工具函数
def validate_ip(ip):
    rule = re.compile("^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if len(ip) > 6:
        if re.match(rule, ip):
            return True
    return False


#发送邮件的工具函数
def sendmail(to_list,title,content):
    try:
        _server = smtplib.SMTP(SMTP_SERVER_HOST,SMTP_SERVER_PORT)
        #_server_conn_starttls() #决定邮件服务器是否开启tls
        _server.ehlo()
        _server.login(SMTP_USER,SMTP_PWD)
        _msg = MIMEText(content,'html','utf-8')
        _msg['Subject'] = Header(title,'utf-8')
        _msg['to'] = Header(';'.join(to_list),'utf-8')
        _msg['From'] = Header('运维:刘宝宝<%s>' % SMTP_USER,'utf-8')
        _msg['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _server.sendmail(SMTP_USER,to_list,_msg.as_string())
        _server.quit()
        return {'code': 0, 'sucmsg': '申请相关信息已经发至您的邮箱,请注意查收!'}
    except:
        return {'code': 1, 'errmsg': '邮箱地址不存在,请核实后再输入!'}




#插入旧的数据

def insert_into_old():
    print os.path.realpath(__file__)


#测试代码
if __name__ == "__main__":
    #sendmail(['liujiabao521314@163.com'],'申请资源','申请资源列表')
    print insert_into_old()
