#encoding:utf-8
import sys
reload(sys)
import ipahttp
sys.setdefaultencoding( "utf-8" )
from flask import Flask,request,session,render_template,redirect
from  web import app
import requests,json
import utils
import apply_utils
import requests,json

def validate_apply_res(mail,name,reark):
    if str(mail).strip() == '':
        return {'code':1,'errmsg':'邮件的名字不能为空或者空格和空字符!'}
    elif str(name).strip() == '':
        return {'code':1,'errmsg':'您的姓名不能为空或者空格和空字符!'}
    elif str(reark).strip() == '':
        return {'code':1,'errmsg':'备注不能为空或者空格和空字符!'}
    return {'code':0,'sucmsg':'正确'}



def validate_apply_acc(mail,name):
    if str(mail).strip() == '':
        return {'code':1,'errmsg':'邮件的名字不能为空或者空格和空字符!'}
    elif str(name).strip() == '':
        return {'code':1,'errmsg':'您的姓名不能为空或者空格和空字符!'}
    return {'code':0,'sucmsg':'正确'}


#调用freeipa的接口
def transfer_freeipa(login_name,name,depment):
    ipa = ipahttp.ipa('freeipa66.xhj.com')
    ipa.login('admin','yunniao.me')
    ipa_find = ipa.user_find(login_name)
    if ipa_find['result']['summary'][0] == '0':
        ipa.user_add(login_name,
                     {"cn": name, "givenname":name, "displayname": name, "gecos": name, "initials": name,
                      "krbprincipalname": "%s@XHJ.COM" % login_name, "sn": name[0], "userpassword": login_name})
        ipa.group_add_member(depment, login_name, 'user')
        return True
    else:
        ipa.group_add_member(depment, login_name, 'user')
        return False


#删除资产记录的时候删除对应freeipa的主机
def del_host_freeipa(host_name):
    ipa = ipahttp.ipa('freeipa66.xhj.com')
    ipa.login('admin','yunniao.me')
    ipahost_find = ipa.host_find(host_name)
    if ipahost_find['result']['summary'][0] == '1':
        e = ipa.host_del(host_name)
        print e
        return True
    else:
        return False





if __name__ == "__main__":
    pass
