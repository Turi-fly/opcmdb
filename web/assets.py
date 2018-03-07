#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from flask import Flask,request,session,render_template,redirect
from  . import app
import requests,json
import utils
import csv
from functools import wraps
from StringIO import StringIO
import time

headers = {'content-type': 'application/json'}

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('author','nologin') == 'nologin':
            return redirect('/login')
        rt = func(*args, **kwargs)
        return rt
    return wrapper

'''
查看硬件资产列表
'''
@app.route("/assets/hw_list/",methods=['POST','GET'])
@login_required
def assets_hw_list():
    data_asset = utils.api_action('asset.list',{'where':{'status':0}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list',{'where':{'status':0}})
    idc_list = json.loads(data_idc).get('result',{})
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model',['id','model'])
    for model in model_list:
         _model_list[model['id']] = model['model']
    raid_list  = app.config['cursor'].get_results('raid',['id','raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    return render_template('hw_assets_list.html',assets=assets_list,\
                           idc=_idc_list,\
                           cabinet=_cabinet_list,\
                           model_list=_model_list,\
                           type_list=_type_list,\
                           raid_list=_raid_list,\
                           spec_list=_spec_list
                           )



'''
进行创建资产的dailog
'''
@app.route('/assets/hw_create/', methods=['POST', 'GET'])
@login_required
def create_hw_asset():
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result')
    model_list = app.config['cursor'].get_results('model',['id','model'])
    raid_list  = app.config['cursor'].get_results('raid',['id','raid_level'])
    type_list  = app.config['cursor'].get_results('type',['id','type'])
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    cabinet_list = app.config['cursor'].get_results('cabinet', ['id', 'cabinet_num','position'])
    return render_template('asset_hw_create.html',idc_list=idc_list,\
                           model_list=model_list,\
                           raid_list=raid_list,\
                           type_list=type_list,\
                           spec_list=spec_list,\
                           cabinet_list=cabinet_list
                           )


'''
执行添加资产
'''
@app.route('/assets/add_hw_create/', methods=['POST'])
@login_required
def add_hw_asset():
    dict_data = request.form.to_dict()
    data = utils.api_action('asset.create', dict_data)
    data = json.loads(data)
    return json.dumps(data)


'''
更新资产的dailog
'''
@app.route('/assets/hw_modify/', methods=['POST', 'GET'])
@login_required
def modify_hw_asset():
    id = request.args.get('id')
    data_info = utils.api_action('asset.list', {'where': {'status': 0,'id':id}})
    data_info_assets = json.loads(data_info).get('result',{})
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result')
    model_list = app.config['cursor'].get_results('model',['id','model'])
    type_list =app.config['cursor'].get_results('type',['id','type'])
    spec_list = app.config['cursor'].get_results('spec',['id','spec'])
    cabinet_list = app.config['cursor'].get_results('cabinet',['id','cabinet_num','position','idc_id'])
    raid_list  = app.config['cursor'].get_results('raid',['id','raid_level'])
    return render_template('asset_hw_modify.html',\
                           asset=data_info_assets[0],\
                           idc_list=idc_list,\
                           model_list=model_list,\
                           type_list=type_list,\
                           spec_list=spec_list,\
                           cabinet_list=cabinet_list,\
                           raid_list=raid_list)

'''
进行执行更新资产
'''
@app.route('/assets/modify_hw_create/', methods=['POST', 'GET'])
@login_required
def update_asset_hw():
    dict_data = request.form.to_dict()
    data = {}
    data['data'] = dict_data
    data['where'] = {'id':dict_data['id'],'status':0}
    _data = utils.api_action('asset.update', data)
    _data_re = json.loads(_data)
    return json.dumps(_data_re)


'''
进行删除资产
'''
@app.route('/assets/hw_delete/',methods=['POST', 'GET'])
@login_required
def delete_asset_hw():
    id = request.args.get('id')
    hostname = request.args.get('hostname')
    _data = {}
    _data['data'] = {'status':1}
    _data['where'] = {'id':id}
    _data['hostname'] = hostname
    _data_re = utils.api_action('asset.delete',_data)
    data = json.loads(_data_re)
    return json.dumps(data)



'''
查看idc列表信息
'''
@app.route('/assets/idc_list/', methods=['POST', 'GET'])
@login_required
def get_idc_list():
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result',{})
    return render_template('idc_list.html',idcs=idc_list)


'''
创建idc信息dialog
'''
@app.route('/assets/idc_create/', methods=['POST', 'GET'])
@login_required
def idc_create():
    return render_template('idc_create.html')


'''
执行创建idc操作
'''
@app.route('/assets/add_idc_create/', methods=['POST', 'GET'])
@login_required
def add_idc_create():
    dict_data = request.form.to_dict()
    data = utils.api_action('idc.create', dict_data)
    data = json.loads(data)
    return json.dumps(data)


'''
更新idc信息的dialog
'''
@app.route('/assets/idc_modify/', methods=['GET'])
@login_required
def idc_modify():
    id = request.args.get('id')
    data_info = utils.api_action('idc.list', {'where': {'status':0,'id':id}})
    idc_list = json.loads(data_info).get('result',{})
    return render_template('idc_modify.html',idc=idc_list[0])


'''
执行更新idc信息的dialog
'''
@app.route('/assets/update_idc_list/', methods=['POST', 'GET'])
@login_required
def update_idc_list():
    dict_data = request.form.to_dict()
    data = {}
    data['data'] = dict_data
    data['where'] = {'id':dict_data['id']}
    _data = utils.api_action('idc.update', data)
    _data_re = json.loads(_data)
    return json.dumps(_data_re)


'''
进行删除idc信息
'''
@app.route('/assets/idc_delete/', methods=['POST', 'GET'])
@login_required
def idc_delete():
    id = request.args.get('id')
    _data = {}
    _data['data'] = {'status':1}
    _data['where'] = {'id':id}
    _data_re = utils.api_action('idc.delete',_data)
    data = json.loads(_data_re)
    return json.dumps(data)



'''
查看机柜信息
'''
@app.route('/assets/cabinet_list/', methods=['POST', 'GET'])
@login_required
def cabinet_list():
    data = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data).get('result',{})
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result',{})
    _idc_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    return render_template('cabinet_list.html',cabinets=cabinet_list,idc_list=_idc_list)



'''
创建机柜的显示dailog页面
'''
@app.route('/assets/cabinet_create/', methods=['POST', 'GET'])
@login_required
def cabinet_create():
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result',{})
    return render_template('cabinet_create.html',idc_list=idc_list)


'''
进行创建机柜信息
'''
@app.route('/assets/add_cabinet_create/',methods=['POST','GET'])
@login_required
def add_cabinet_create():
    dict_data = request.form.to_dict()
    data = utils.api_action('cabinet.create', dict_data)
    data = json.loads(data)
    return json.dumps(data)



'''
进行更新机柜的显示dailog的页面
'''
@app.route('/assets/cabinet_modify/',methods=['POST','GET'])
@login_required
def cabinet_modify():
    id = request.args.get('id')
    data_info = utils.api_action('cabinet.list', {'where': {'id': id}})
    cabinet_list = json.loads(data_info).get('result',{})
    data = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data).get('result',{})
    return render_template('cabinet_modify.html',cabinet=cabinet_list[0],idc_list=idc_list)


'''
进行更新机柜信息
'''
@app.route('/assets/update_cabinet_modify/',methods=['POST','GET'])
@login_required
def update_cabinet_modify():
    dict_data = request.form.to_dict()
    data = {}
    data['data'] = dict_data
    data['where'] = {'id':dict_data['id']}
    _data = utils.api_action('cabinet.update', data)
    _data_re = json.loads(_data)
    return json.dumps(_data_re)



'''
进行删除机柜信息
'''
@app.route('/assets/cabinet_delete/',methods=['POST','GET'])
@login_required
def delete_cabinet():
    id = request.args.get('id')
    _data = {}
    _data['where'] = {'id':id}
    _data_re = utils.api_action('cabinet.delete',_data)
    data = json.loads(_data_re)
    return json.dumps(data)


'''
查看vm列表
'''
@app.route('/assets/vm_list/',methods=['POST','GET'])
@login_required
def get_vm_list():
    data = utils.api_action('vm.list', {'where': {'status': 0}})
    vm_list = json.loads(data).get('result',{})
    data_asset = utils.api_action('asset.list',{'where':{'status':0}})
    asset_list = json.loads(data_asset).get('result',{})
    des_use_list = app.config['cursor'].get_results('des_use', ['id', 'identity'])
    _asset_list = {}
    _des_use_list = {}
    for asset in asset_list:
        _asset_list[asset['id']] = asset['inner_ip']
    for des_use in des_use_list:
                _des_use_list[des_use['id']] = des_use['identity']
    return render_template('vm_list.html',vms=vm_list,asset_list=_asset_list,des_use_list=_des_use_list)



'''
创建vm信息dialog
'''
@app.route('/assets/vm_create/',methods=['POST','GET'])
@login_required
def vm_create():
    data = utils.api_action('asset.list', {'where': {'status': 0}})
    asset_list = json.loads(data).get('result',{})
    return render_template('vm_create.html',asset_list=asset_list)



'''
执行创建vm的信息
'''
@app.route('/assets/add_vm_create/',methods=['POST','GET'])
@login_required
def add_vm_create():
    dict_data = request.form.to_dict()
    data = utils.api_action('vm.create', dict_data)
    data = json.loads(data)
    return json.dumps(data)



'''
更新的dialog
'''
@app.route('/assets/vm_modify/',methods=['POST','GET'])
@login_required
def vm_modify():
    id = request.args.get('id')
    data_info = utils.api_action('vm.list', {'where': {'id': id,'status':0}})
    vm = json.loads(data_info).get('result',{})
    data = utils.api_action('asset.list', {'where': {'status': 0}})
    asset_list = json.loads(data).get('result',{})
    des_use_list = app.config['cursor'].get_results('des_use', ['id', 'identity'])
    return render_template('vm_modify.html',asset_list=asset_list,vm=vm[0],des_use_list=des_use_list)



'''
执行更新dialog
'''
@app.route('/assets/update_vm_modify/',methods=['POST','GET'])
@login_required
def update_vm_modify():
    dict_data = request.form.to_dict()
    data = {}
    data['data'] = dict_data
    data['where'] = {'id':dict_data['id']}
    _data = utils.api_action('vm.update', data)
    _data_re = json.loads(_data)
    return json.dumps(_data_re)



'''
删除vm
'''
@app.route('/assets/vm_delete/',methods=['POST','GET'])
@login_required
def vm_delete():
    id = request.args.get('id')
    vm = request.args.get('vm')
    _data = {}
    _data['data'] = {'status':1}
    _data['where'] = {'id':id}
    _data['vm'] = vm
    _data_re = utils.api_action('vm.delete',_data)
    data = json.loads(_data_re)
    return json.dumps(data)



'''
下载所有硬件资产信息
'''
@app.route('/assets/download/',methods=["GET"])
@login_required
def assets_download():
    data_asset = utils.api_action('asset.list',{'where':{'status':0}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list',{'where':{'status':0}})
    idc_list = json.loads(data_idc).get('result')
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model',['id','model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
        raid_list  = app.config['cursor'].get_results('raid',['id','raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    s = StringIO()
    header = '机房,机柜机位信息,服务器规格,sn编号,供应商,型号,管理IP地址,应用IP地址,远程管理卡IP,主机名,操作系统,CPU个数核数,内存个数,内存槽数,硬盘个数,硬盘槽数,内存(MB),硬盘大小(GB),硬盘类型,raid级别,raid卡类型,使用人,业务,出厂日期,保修日期'.split(',')
    _header = 'idc_id,cabinet_seat_id,spec_id,sn,type_id,model_id,inner_ip,app_ip,remote_ip,hostname,os,cpu,nu_ram,slot_ram,nu_disk,slot_disk,ram,disk,disk_type,raid_id,raid_type,admin,business,purchase_date,warranty'.split(',')
    csv_writer = csv.writer(s)
    csv_writer.writerow(header)
    for asset in assets_list:
        _tmp_list = []
        for head in _header:
            if head == 'idc_id':
                _tmp_list.append(_idc_list.get(asset.get('idc_id'),' '))
            elif head == 'cabinet_seat_id':
                _tmp_list.append(_cabinet_list.get(asset.get('cabinet_seat_id'),' '))
            elif head == 'spec_id':
                _tmp_list.append(_spec_list.get(asset.get('spec_id'),' '))
            elif head == 'model_id':
                _tmp_list.append(_model_list.get(asset.get('model_id'),' '))
            elif head == 'type_id':
                _tmp_list.append(_type_list.get(asset.get('type_id'),' '))
            elif head == 'raid_id':
                _tmp_list.append(_raid_list.get(asset.get('raid_id'),' '))
            else:
                _tmp_list.append(asset.get(head,' '))
        csv_writer.writerow(_tmp_list)
    cxt = s.getvalue()
    s.close()
    return cxt,\
            200,\
            {
                'Content-Type' : 'text/csv; charset=GBK',
                'Content-Disposition' : 'attachment;filename=all_assets_%s.csv' %(time.strftime('%Y-%m-%d-%H:%M'))

                    }

'''
下载搜索资产列表
'''
@app.route('/assets/part_download/',methods=['GET','POST'])
@login_required
def assets_part_download():
    data = request.args.to_dict()
    data_asset = utils.api_action('asset.list',{'where':{'status':0,'id':data.values()}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list',{'where':{'status':0}})
    idc_list = json.loads(data_idc).get('result')
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model',['id','model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
    raid_list  = app.config['cursor'].get_results('raid',['id','raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    s = StringIO()
    header = '机房,机柜机位信息,服务器规格,sn编号,供应商,型号,管理IP地址,应用IP地址,远程管理卡IP,主机名,操作系统,CPU个数核数,内存个数,内存槽数,硬盘个数,硬盘槽数,内存(MB),硬盘大小(GB),硬盘类型,raid级别,raid卡类型,使用人,业务,出厂日期,保修日期'.split(',')
    _header = 'idc_id,cabinet_seat_id,spec_id,sn,type_id,model_id,inner_ip,app_ip,remote_ip,hostname,os,cpu,nu_ram,slot_ram,nu_disk,slot_disk,ram,disk,disk_type,raid_id,raid_type,admin,business,purchase_date,warranty'.split(',')
    csv_writer = csv.writer(s)
    csv_writer.writerow(header)
    for asset in assets_list:
        _tmp_list = []
        for head in _header:
            if head == 'idc_id':
                _tmp_list.append(_idc_list.get(asset.get('idc_id'),' '))
            elif head == 'cabinet_seat_id':
                _tmp_list.append(_cabinet_list.get(asset.get('cabinet_seat_id'),' '))
            elif head == 'spec_id':
                _tmp_list.append(_spec_list.get(asset.get('spec_id'),' '))
            elif head == 'model_id':
                _tmp_list.append(_model_list.get(asset.get('model_id'),' '))
            elif head == 'type_id':
                _tmp_list.append(_type_list.get(asset.get('type_id'),' '))
            elif head == 'raid_id':
                _tmp_list.append(_raid_list.get(asset.get('raid_id'),' '))
            else:
                _tmp_list.append(asset.get(head,' '))
        csv_writer.writerow(_tmp_list)
    cxt = s.getvalue()
    s.close()
    return cxt,\
           200,\
            {
                'Content-Type' : 'text/csv; charset=UTF-8',
                'Content-Disposition' : 'attachment;filename=search_assets_%s.csv' %(time.strftime('%Y-%m-%d-%H:%M'))

                    }




"""
下载虚拟机资产列表
"""
@app.route('/assets/vm_download/',methods=['GET'])
@login_required
def vm_download():
   data = utils.api_action('vm.list', {'where': {'status': 0}})
   vm_list = json.loads(data).get('result',{})
   data_asset = utils.api_action('asset.list',{'where':{'status':0}})
   asset_list = json.loads(data_asset).get('result',{})
   _asset_list = {}
   for asset in asset_list:
       _asset_list[asset['id']] = asset['inner_ip']
   s = StringIO()
   header = 'vm名称,ip,网卡mac地址,uuid,cpu,内存,硬盘,使用人,宿主机,业务,备注'.split(',')
   _header = 'vm,ip,mac,uuid,cpu,ram,disk,admin,host_id,business,remark'.split(',')
   csv_writer = csv.writer(s)
   csv_writer.writerow(header)
   for vm in vm_list:
        _tmp_list = []
        for head in _header:
            if head == 'host_id':
                _tmp_list.append(_asset_list.get(vm.get('host_id'),' '))
            else:
                _tmp_list.append(vm.get(head,' '))
        csv_writer.writerow(_tmp_list)
   cxt = s.getvalue()
   s.close()
   return cxt,\
         200,\
         {
            'Content-Type' : 'text/csv; charset=UTF-8',
            'Content-Disposition' : 'attachment;filename=vm_assets_%s.csv' %(time.strftime('%Y-%m-%d-%H:%M'))

                     }




"""
下载虚拟机下载资产列表
"""
@app.route('/assets/vm_part_download/',methods=['GET'])
@login_required
def vm_part_download():
    data = request.args.to_dict()
    data_vm = utils.api_action('vm.list',{'where':{'status':0,'id':data.values()}})
    vm_list = json.loads(data_vm).get('result',{})
    data_asset = utils.api_action('asset.list',{'where':{'status':0}})
    asset_list = json.loads(data_asset).get('result',{})
    _asset_list = {}
    for asset in asset_list:
        _asset_list[asset['id']] = asset['inner_ip']
    s = StringIO()
    header = 'vm名称,ip,网卡mac地址,uuid,cpu,内存,硬盘,使用人,宿主机,业务,备注'.split(',')
    _header = 'vm,ip,mac,uuid,cpu,ram,disk,admin,host_id,business,remark'.split(',')
    csv_writer = csv.writer(s)
    csv_writer.writerow(header)
    for vm in vm_list:
         _tmp_list = []
         for head in _header:
             if head == 'host_id':
                 _tmp_list.append(_asset_list.get(vm.get('host_id'),' '))
             else:
                 _tmp_list.append(vm.get(head,' '))
         csv_writer.writerow(_tmp_list)
    cxt = s.getvalue()
    s.close()
    return cxt,\
           200,\
         {
             'Content-Type' : 'text/csv; charset=UTF-8',
             'Content-Disposition' : 'attachment;filename=search_vm_assets_%s.csv' %(time.strftime('%Y-%m-%d-%H:%M'))
             }



'''
数据初始化成表格
'''
@app.route('/assets/data_view1/',methods=['GET','POST'])
@login_required
def data_view1(**kwargs):
    data = request.form.to_dict()
    data_asset = utils.api_action('asset.list',{'where':{'status':0,'idc_id':data['name']}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data_idc).get('result', {})
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model', ['id', 'model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
    raid_list = app.config['cursor'].get_results('raid', ['id', 'raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    return render_template('data_view_index1.html', assets=assets_list, \
                          idc=_idc_list, \
                          cabinet=_cabinet_list, \
                          model_list=_model_list, \
                          type_list=_type_list, \
                          raid_list=_raid_list, \
                          spec_list=_spec_list
                          )


@app.route('/assets/data_view2/',methods=['GET','POST'])
@login_required
def data_view2(**kwargs):
    data = request.form.to_dict()
    data_asset = utils.api_action('asset.list',{'where':{'status':0,'idc_id':data['name'],'model_id':data['model_id']}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data_idc).get('result', {})
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model', ['id', 'model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
    raid_list = app.config['cursor'].get_results('raid', ['id', 'raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    return render_template('data_view_index1.html', assets=assets_list, \
                          idc=_idc_list, \
                          cabinet=_cabinet_list, \
                          model_list=_model_list, \
                          type_list=_type_list, \
                          raid_list=_raid_list, \
                          spec_list=_spec_list
                          )



@app.route('/assets/data_view3/',methods=['GET','POST'])
@login_required
def data_view3(**kwargs):
    data = request.form.to_dict()
    data_asset = utils.api_action('asset.list',{'where':{'status':0,'idc_id':data['name'],'spec_id':data['spec_id']}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data_idc).get('result', {})
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model', ['id', 'model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
    raid_list = app.config['cursor'].get_results('raid', ['id', 'raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    return render_template('data_view_index1.html', assets=assets_list, \
                          idc=_idc_list, \
                          cabinet=_cabinet_list, \
                          model_list=_model_list, \
                          type_list=_type_list, \
                          raid_list=_raid_list, \
                          spec_list=_spec_list
                          )


@app.route('/assets/data_view4/',methods=['GET','POST'])
@login_required
def data_view4(**kwargs):
    data = request.form.to_dict()
    data_asset = utils.api_action('asset.list',{'where':{'status':0,'idc_id':data['name'],'cabinet_seat_id':data['cabinet_id']}})
    assets_list = json.loads(data_asset).get('result',{})
    data_idc = utils.api_action('idc.list', {'where': {'status': 0}})
    idc_list = json.loads(data_idc).get('result', {})
    _idc_list = {}
    _cabinet_list = {}
    _model_list = {}
    _raid_list = {}
    _type_list = {}
    _spec_list = {}
    for idc in idc_list:
        _idc_list[idc['id']] = idc['name']
    data_cabinet = utils.api_action('cabinet.list')
    cabinet_list = json.loads(data_cabinet).get('result')
    for cabinet in cabinet_list:
        _cabinet_list[cabinet['id']] = cabinet['cabinet_num']
    model_list = app.config['cursor'].get_results('model', ['id', 'model'])
    for model in model_list:
        _model_list[model['id']] = model['model']
    raid_list = app.config['cursor'].get_results('raid', ['id', 'raid_level'])
    for raid in raid_list:
        _raid_list[raid['id']] = raid['raid_level']
    spec_list = app.config['cursor'].get_results('spec', ['id', 'spec'])
    for spec in spec_list:
        _spec_list[spec['id']] = spec['spec']
    type_list = app.config['cursor'].get_results('type', ['id', 'type'])
    for type in type_list:
        _type_list[type['id']] = type['type']
    return render_template('data_view_index1.html', assets=assets_list, \
                          idc=_idc_list, \
                          cabinet=_cabinet_list, \
                          model_list=_model_list, \
                          type_list=_type_list, \
                          raid_list=_raid_list, \
                          spec_list=_spec_list
                          )