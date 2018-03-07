#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import request,render_template
from  . import app
import json,traceback
import utils
import apply_utils


'''
申请资源导航页
'''
@app.route("/Apply/resource/",methods=['GET'])
def Apply_resource():
    # use_list = app.config['cursor'].get_results('des_use', ['id', 'identity'])
    return render_template("apply_index.html")


'''
申请资源列表页
'''
@app.route("/Apply/list/",methods=['GET'])
def Apply_list():
    data = utils.api_action('vm.list', {'where': {'status': 0}})
    vm_list = json.loads(data).get('result',{})
    use_list = app.config['cursor'].get_results('des_use',['id','identity'])
    use_list_dic = {}
    for use in use_list:
        use_list_dic[use['id']] = use['identity']
    return render_template('apply_list.html',vms=vm_list,use_list=use_list_dic)


'''
申请虚拟机列表
'''
@app.route("/Apply/vm/",methods=['POST','GET'])
def Apply_vm():
    mail = request.form.get('mail','')
    mail_text = mail
    name = request.form.get('name','')
    remark = request.form.get('remark','')
    des_use_id = request.form.get('use_id','')
    exists_acc = app.config['cursor'].get_one_result('account_cnt', ['id'],
                                                       {'accounts':mail_text})
    _status = apply_utils.validate_apply_res(mail,name,remark)
    if not exists_acc:
        if _status['code'] == 0:
            mail += "@yunniao.me"
            _status_code = utils.sendmail([mail], '', '')
            if _status_code['code'] == 0:
                _res_list = app.config['cursor'].get_one_result('vm', ['id', 'ip', 'vm', 'admin', 'remark'], {'use_status': 0,'des_use_id':des_use_id},
                                                                   limit=1)
                if _res_list:
                    app.config['cursor'].execute_insert_sql('account_cnt', {'accounts': mail_text})
                    id = _res_list['id']
                    ip = _res_list['ip']
                    vm = _res_list['vm']
                    _is_ok = apply_utils.transfer_freeipa(mail_text,name,'dev')
                    app.config['cursor'].execute_update_sql('vm',{"admin":name,"remark":remark,"use_status":1},{'id':id})
                    title = '%s申请的虚拟机资源' % name
                    if not _is_ok:
                        content = '虚拟机名称:%s,ip地址:%s,账号:%s,密码:%s' %(vm,ip,mail_text,'您的账号已经存在密码不在是初始化密码,要是没有更改还是%s' % mail_text)
                    else:
                        content = '虚拟机名称:%s,ip地址:%s,账号:%s,密码:%s' % (vm, ip, mail_text, mail_text)
                    _status_code = utils.sendmail([mail],title,content)
                    return json.dumps(_status_code)
                else:
                    return json.dumps({'code':1,'errmsg':'虚拟机已经没有了,请联系运维刘宝宝来开通!'})
            else:
                return json.dumps(_status_code)
        else:
            return json.dumps(_status)
    else:
        return json.dumps({'code':1,'errmsg':'您已经申请过虚拟机!每人只能拥有一台!'})


'''
申请账号导航页
'''
@app.route("/Apply/account_nav/",methods=['POST','GET'])
def Apply_account_nav():
    return render_template("apply_account.html")


'''
申请页面的列表页
'''
@app.route("/Apply/account/",methods=['POST','GET'])
def Apply_account():
    mail = request.form.get('mail','')
    mail_text = mail
    name = request.form.get('name','')
    depment_id = request.form.get('depment_id','')

    exists_acc = app.config['cursor'].get_one_result('account_cnt', ['accounts'],
                                                     {'accounts':mail})

    depment_list = app.config['cursor'].get_one_result('depment', ['depment'],
                                                       {'id':depment_id})

    _status = apply_utils.validate_apply_acc(name,mail)
    content = '''
                 账号:%s,密码:%s
                 连接方式如下:
                 公司内网
                    1.从通过跳板机登录虚机的使用方法：
                        ssh  %s@192.168.200.200
                    2.不通过跳板机的方式:
                        ssh  %s@192.168.200.xx(相关机器的IP)
                 公司外网:
                    1.ssh -p 53122 %s@vpnx.xunhuji.me

              ''' %(mail_text,mail_text,mail_text,mail_text,mail_text)
    if not exists_acc:
        if _status['code'] == 0:
            mail += "@yunniao.me"
            _status_code = utils.sendmail([mail], '', '')
            title = '%s申请的账号' % name
            if _status_code['code'] == 0:
                for _depment in ['dev','qa','ops']:
                    if depment_list['depment']  == _depment:
                        try:
                            _is_ok = apply_utils.transfer_freeipa(mail_text,name,_depment)
                            if _is_ok:
                                _status_code = utils.sendmail([mail], title, content)
                                return json.dumps(_status_code)
                            else:
                                return json.dumps({'code':1,'errmsg':'您已经有自己的账号了!'})
                        except:
                            return json.dumps({'code':1,'errmsg':traceback.format_exc()})
            else:
                return json.dumps(_status_code)
        else:
            return json.dumps(_status)
    else:
        return json.dumps({'code':1,'errmsg':'您已经有自己的账号了!'})




"""
虚机使用说明文档
"""
@app.route("/Apply/vmManual/",methods=['GET'])
def Apply_vmManual():
    return render_template('apply_vmManual.html')
#@app.route("/Apply/xx/",methods=['POST','GET'])
#def Apply_xx():
#    file = open('/data/yn_cmdb_v1/web/features.txt', 'r')
#    for line in file.readlines():
#        line_list = line.split()
#        print line_list
#        app.config['cursor'].execute_update_sql('vm', {"admin": line_list[1], "remark":line_list[2], "use_status": 1},
#                                                 {'ip': line_list[0]})
#    return '1'


# @app.route("/Apply/xx/",methods=['POST','GET'])
# def Apply_xx():
#     app.config['cursor'].execute_insert_sql('des_use',{'identity':'测试机'})
#     return '1'

