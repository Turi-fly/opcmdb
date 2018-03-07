#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import request
from . import app ,jsonrpc
import utils
#from auth import auth_login
import json, traceback
from web.apply_utils import del_host_freeipa
from collections import Counter


'''
查看资产列表的api
'''
@jsonrpc.method('asset.list')
def get_asset_list(**kwargs):
    try:
        #指定输出的内容列表
        output = [
                  'id','sn','inner_ip',
                  'app_ip','remote_ip',
                  'mac','hostname',
                  'os','cpu','nu_ram','nu_disk','ram',
                  'disk','idc_id',
                  'model_id','raid_id',
                  'raid_type','admin',
                  'spec_id','type_id',
                  'business','remote_card',
                  'purchase_date','warranty',
                  'remark','nu_cpu','cabinet_seat_id','disk_type','slot_ram','slot_disk'
                  ]
        #对传入的参数进行接收数据
        data=request.get_json()['params']
        #api可以指定输出字段，如果没有指定output，就按默认output输出
        fields = data.get('output',output)
        # 前端传来的where条件
        where = data.get('where',None)
        #如果没有传入where的值或者是空的情况
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        #进行操作查出数据的内容
        result = app.config['cursor'].get_results('asset',fields,where)
        #写入日志
        utils.write_log('api').info('View all assets')
        #如果结果没有的话
        if not result :
            return json.dumps({'code':1, 'errmsg':'asset  not  exist'})
        #进行对时间字符编码转换
        for _result in result:
            _result['warranty'] = utils.default(_result['warranty'])
            _result['purchase_date'] = utils.default(_result['purchase_date'])
        return json.dumps({'code':0,'result':result})
    except:
        #捕捉异常
        utils.write_log('api').error("View asset error: %s" % traceback.format_exc())
        return json.dumps({'code':  1, 'errmsg': 'View asset failed'})



'''
添加资产的api
'''
@jsonrpc.method('asset.create')
def create_asset(*arg, **kwargs):
    try:
        #指定输出内容
        output = [
                  'os', 'cpu', 'nu_ram', 'nu_disk', 'ram'
                  ]
        #获取前端参数的值
        data = request.get_json()['params']
        #进行对数据的检查是否符合需求
        for _key in 'sn,inner_ip,hostname,os,ram,cpu,disk'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'ram,disk'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        if app.config['cursor'].get_one_result('asset',output,{'sn':data['sn'],'status':0}):
            return json.dumps({'code': 1, 'errmsg': "sn already is exist!"})
        if app.config['cursor'].get_one_result('asset',output,{'hostname':data['hostname'],'status':0}):
            return json.dumps({'code': 1, 'errmsg': "hostname already is exist!"})
        if not utils.validate_ip(data['inner_ip']):
            return json.dumps({'code': 1, 'errmsg': "Inner IP does not conform to the rules!"})
        # if not utils.validate_ip(data['app_ip']):
        #     return json.dumps({'code': 1, 'errmsg': "Application IP does not conform to the rules!"})
        # if not utils.validate_ip(data['remote_ip']):
        #     return json.dumps({'code': 1, 'errmsg': "Remote IP does not conform to the rules!"})
        # if not app.config['cursor'].get_one_result('idc',['name'],{'id':data['idc_id']}):
        #     return json.dumps({'code': 1, 'errmsg': "Idc_id is not exist"})
        #执行插入数据
        app.config['cursor'].execute_insert_sql('asset', data)
        #执行记录日志
        utils.write_log('api').info("create asset success: %s" % data['sn'])
        return json.dumps({'code': 0, 'result': 'create server assets success!'})
    except:
        #捕捉异常
        utils.write_log('api').error("Create asset error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Create asset failed'})



'''
更新资产的api
'''
@jsonrpc.method('asset.update')
def update_asset(*arg, **kwargs):
    try:
        #获取前端传来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where',None)
        #获取要更新这条的数据
        data = data.get('data',None)
        #指定输出的内容
        output = [
            'id','os', 'cpu', 'nu_ram', 'nu_disk', 'ram'
        ]
        #对进行传入的数据进行检查书否符合需求
        for _key in 'sn,inner_ip,hostname,os,ram,cpu,disk'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'ram,disk'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        if app.config['cursor'].get_one_result('asset',output, {'sn': data['sn'],'status':0}) and app.config['cursor'].get_one_result('asset',output, {'sn': data['sn'],'status':0})['id'] != app.config['cursor'].get_one_result('asset',output, {'id': data['id'],'status':0})['id']:
            return json.dumps({'code': 1, 'errmsg': "sn already is exist!"})
        if app.config['cursor'].get_one_result('asset',output, {'hostname': data['hostname'],'status':0}) and app.config['cursor'].get_one_result('asset',output, {'hostname': data['hostname'],'status':0})['id'] != app.config['cursor'].get_one_result('asset',output, {'id': data['id'],'status':0})['id']:
            return json.dumps({'code': 1, 'errmsg': "hostname already is exist!"})
        if not utils.validate_ip(data['inner_ip']):
            return json.dumps({'code': 1, 'errmsg': "Inner IP does not conform to the rules!"})
        # if not utils.validate_ip(data['app_ip']):
        #     return json.dumps({'code': 1, 'errmsg': "Application IP does not conform to the rules!"})
        # if not utils.validate_ip(data['remote_ip']):
        #     return json.dumps({'code': 1, 'errmsg': "Remote IP does not conform to the rules!"})
        # if not app.config['cursor'].get_one_result('idc', ['name'], {'id': data['idc_id']}):
        #     return json.dumps({'code': 1, 'errmsg': "Idc_id is not exist"})
        #进行更新数据
        _data = app.config['cursor'].get_one_result('changelog',output,where)
        app.config['cursor'].execute_update_sql('asset', data, where)
        __data = app.config['cursor'].get_one_result('changelog',output,where)
        print _data
        print __data
        print set(_data)^set(__data)
        #写入日志
        utils.write_log('api').info("update asset success: %s" % data['sn'])
        return json.dumps({'code': 0, 'result': 'Update server assets success!'})
    except:
        #捕捉异常
        utils.write_log('api').error("Update asset error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Update server assets failed'})


'''
删除资产的api(逻辑删除)
'''
@jsonrpc.method('asset.delete')
def delete_asset(**kwargs):
    try:
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #获取硬件的主机名
        hostname = data.get('hostname',None)
        #获取要删除的数据
        data = data.get('data', None)
        #进行删除
        app.config['cursor'].execute_update_sql('asset', data, where)
        utils.write_log('api').info("delete asset success: %s" % hostname )
        _data = app.config['cursor'].get_one_result('asset',where)
        print _data
        if del_host_freeipa(hostname):
        # 执行记录日志
            return json.dumps({'code': 0, 'result': 'Delete asset success!'})
        else:
            return json.dumps({'code': 0, 'result': 'Delete asset success but freeipa dont delete host!'})
        #执行记录日志
    except:
        #捕捉异常
        utils.write_log('api').error("Delete asset error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Delete asset failed'})



'''
查看vm列表的接口
'''
@jsonrpc.method('vm.list')
def get_vm_list(**kwargs):
    try:
        #指定输出的内容列表
        output = [
            'id','uuid','ip','mac','cpu','ram','disk','vm','host_id','business','admin','remark','status','use_status','des_use_id'
        ]
        #对传入的参数进行接收数据
        data=request.get_json()['params']
        #api可以指定输出字段，如果没有指定output，就按默认output输出
        fields = data.get('output',output)
        # 前端传来的where条件
        where = data.get('where',None)
        #如果没有传入where的值或者是空的情况
        if not where:
            return json.dumps({'code':1, 'errmsg':'must need a condition'})
        #进行操作查出数据的内容
        result = app.config['cursor'].get_results('vm', fields, where)
        #写入日志
        utils.write_log('api').info('View all vm')
        #如果结果没有的话
        if not result :
            return json.dumps({'code':1, 'errmsg':'vm  not  exist'})
        return json.dumps({'code':0,'result':result})
    except:
        #捕捉异常
        utils.write_log('api').error("View vm error: %s" % traceback.format_exc())
        return json.dumps({'code':  1, 'errmsg': 'View vm failed'})



'''
创建vm api接口
'''
@jsonrpc.method('vm.create')
def vm_create(**kwargs):
    try:
        #指定输出内容
        output = [
            'id','uuid','ip','mac','cpu','ram','disk','vm','business','admin','remark','status','host_id'
                  ]
        #获取前端参数的值
        data = request.get_json()['params']
        #进行对数据的检查是否符合需求
        for _key in 'ip,mac,cpu,ram,disk,vm'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'ram,disk'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        # if app.config['cursor'].get_one_result('vm',output,{'uuid':data['uuid']}):
        #     return json.dumps({'code': 1, 'errmsg': "uuid already is exist!"})
        if app.config['cursor'].get_one_result('vm',output,{'ip':data['ip'],'status':0}):
            return json.dumps({'code': 1, 'errmsg': "ip already is exist!"})
        if not utils.validate_ip(data['ip']):
            return json.dumps({'code': 1, 'errmsg': "IP does not conform to the rules!"})
        #执行插入数据
        app.config['cursor'].execute_insert_sql('vm', data)
        #执行记录日志
        utils.write_log('api').info("create vm success: %s" % data['vm'])
        return json.dumps({'code': 0, 'result': 'create server vm success!'})
    except:
        #捕捉异常
        utils.write_log('api').error("Create vm error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Create vm failed'})


'''
更新vm api
'''
@jsonrpc.method('vm.update')
def vm_modify(**kwargs):
    try:
        # 获取前端传来的数据
        data = request.get_json()['params']
        # 获取where条件
        where = data.get('where', None)
        # 获取要更新这条的数据
        data = data.get('data', None)
        # 指定输出的内容
        #output = [
        #    'id', 'uuid', 'ip', 'mac', 'cpu', 'ram', 'disk', 'vm', 'business', 'admin', 'remark', 'status', 'host_id','use_status','des_use_id'
        #]
        # 对进行传入的数据进行检查书否符合需求
        for _key in 'uuid,ip,mac,cpu,ram,disk,vm,host_id'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'ram,disk'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        # if app.config['cursor'].get_one_result('vm',output,{'uuid':data['uuid']}) and \
        #                 app.config['cursor'].get_one_result('vm', output, {'uuid': data['uuid']})['id'] != \
        #                 app.config['cursor'].get_one_result('vm', output, {'id': data['id']})['id']:
        #     return json.dumps({'code': 1, 'errmsg': "uuid already is exist!"})
        if not app.config['cursor'].get_one_result('asset', ['hostname'], {'id': data['host_id'], 'status': 0}):
            return json.dumps({'code': 1, 'errmsg': "hostname is not exist"})
        if not utils.validate_ip(data['ip']):
            return json.dumps({'code': 1, 'errmsg': "IP does not conform to the rules!"})
        # 进行更新数据
        app.config['cursor'].execute_update_sql('vm', data, where)
        # 写入日志
        utils.write_log('api').info("update vm success: %s" % data['vm'])
        return json.dumps({'code': 0, 'result': 'Update server vm success!'})
    except:
        # 捕捉异常
        utils.write_log('api').error("Update vm error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Update server vm failed'})


'''
删除vm api
'''
@jsonrpc.method('vm.delete')
def vm_delete(**kwargs):
    try:
        # 获取前端出来的数据
        data = request.get_json()['params']
        # 获取where条件
        where = data.get('where', None)
        # 获取主机名
        vm = data.get('vm',None)
        # 获取要删除的数据
        data = data.get('data', None)
        # 进行删除
        app.config['cursor'].execute_delete_sql('vm',where)
        utils.write_log('api').info("delete vm success: %s" % vm )
        if del_host_freeipa(vm):
        # 执行记录日志
            return json.dumps({'code': 0, 'result': 'Delete vm success!'})
        else:
            return json.dumps({'code': 0, 'result': 'Delete vm success but freeipa dont delete host!'})
    except:
        # 捕捉异常
        utils.write_log('api').error("Delete vm error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Delete vm failed'})



'''
查看idc列表的接口
'''
@jsonrpc.method('idc.list')
def get_idc_list(**kwargs):
    try:
        #指定输出的字段
        output = [
                'id','name','physical','switch','vm','ip_seg','address','phone','status'
                  ]
        data = request.get_json()['params']
        fields = data.get('output', output)  # api可以指定输出字段，如果没有指定output，就按默认output输出
        where = data.get('where', None)
        #执行查看idc的记录
        result = app.config['cursor'].get_results('idc', fields, where)
        #进行执行日志记录
        utils.write_log('api').info('View all idc')
        if not result:
            return json.dumps({'code': 1, 'errmsg': 'idc  not  exist'})
        return json.dumps({'code': 0, 'result': result})
    except:
        #捕捉异常
        utils.write_log('api').error("View all idc: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'View idc all failed'})



'''
创建idc列表的接口
'''
@jsonrpc.method('idc.create')
def create_idc(**kwargs):
    try:
        output = [
            'id','name','status','address','phone','physical','switch','vm','ip_seg'
        ]
        data = request.get_json()['params']
        if app.config['cursor'].get_one_result('idc', output, {'name': data['name'],'status':0}):
            return json.dumps({'code': 1, 'errmsg': "idc name already is exist!"})
        for _key in 'name,address,phone,physical,switch,vm,ip_seg'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'physical,switch,vm'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        result = app.config['cursor'].execute_insert_sql('idc', data)
        #记录日志
        utils.write_log('api').info("create idc success: %s" % data['name'])
        return json.dumps({'code': 0, 'result': "create idc success: %s" % data['name']})
    except:
        #捕捉异常
        utils.write_log('api').error("create idc: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'create idc failed'})



'''
更新idc api
'''
@jsonrpc.method('idc.update')
def update_idc(**kwargs):
    try:
        # 获取前端传来的数据
        data = request.get_json()['params']
        # 获取where条件
        where = data.get('where', None)
        # 获取要更新这条的数据
        data = data.get('data', None)
        # 指定输出的内容
        output = [
            'id', 'name', 'status'
        ]
        # 对进行传入的数据进行检查书否符合需求
        if app.config['cursor'].get_one_result('idc', output, {'name': data['name'],'status':0}) and app.config['cursor'].get_one_result('idc', output, {'name': data['name'],'status':0})['id'] != app.config['cursor'].get_one_result('idc', output, {'id': data['id'],'status':0})['id']:
            return json.dumps({'code': 1, 'errmsg': "idc name already is exist!"})
        for _key in 'name,address,phone,physical,switch,vm,ip_seg'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'physical,switch,vm'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        # 进行更新数据
        app.config['cursor'].execute_update_sql('idc', data, where)
        # 写入日志
        utils.write_log('api').info("update idc success: %s" % data['name'])
        return json.dumps({'code': 0, 'result': 'Update idc assets success!'})
    except:
        # 捕捉异常
        utils.write_log('api').error("Update idc error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Update idc failed'})


'''
删除机房列表api
'''
@jsonrpc.method('idc.delete')
def delete_idc(**kwargs):
    try:
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #获取要删除的数据
        data = data.get('data', None)
        #进行删除
        app.config['cursor'].execute_update_sql('idc', data, where)
        #执行记录日志
        utils.write_log('api').info("delete idc success: %s" % data['name'])
        return json.dumps({'code': 0, 'result': 'Delete idc success!'})
    except:
        #捕捉异常
        utils.write_log('api').error("Delete asset error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Delete idc failed'})




'''
展示机柜的列表
'''
@jsonrpc.method('cabinet.list')
def cabinet_list(**kwargs):
    try:
        output = [
            'id','cabinet_num','position','idc_id','physical','switch','vm'
        ]
        # 对传入的参数进行接收数据
        data = request.get_json()['params']
        # api可以指定输出字段，如果没有指定output，就按默认output输出
        fields = data.get('output', output)
        # 前端传来的where条件
        where = data.get('where', None)
        result = app.config['cursor'].get_results('cabinet', fields, where)
        utils.write_log('api').info('View all cabinet')
        return json.dumps({'code': 0, 'result': result})
    except:
        utils.write_log('api').error("View cabinet error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'View cabinet failed'})



'''
创建机柜api
'''
@jsonrpc.method('cabinet.create')
def cabinet_create(**kwargs):
    try:
        # 指定输出内容
        output = [
            'id','cabinet_num','position','idc_id','physical','switch','vm'
        ]
        # 获取前端参数的值
        data = request.get_json()['params']
        # 进行对数据的检查是否符合需求
        for _key in 'physical,switch,vm,cabinet_num'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'physical,switch,vm'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        if app.config['cursor'].get_one_result('cabinet', output, {'cabinet_num': data['cabinet_num']}):
            return json.dumps({'code': 1, 'errmsg': "cabinet_num already is exist!"})
        # 执行插入数据
        app.config['cursor'].execute_insert_sql('cabinet', data)
        # 执行记录日志
        utils.write_log('api').info("create asset success: %s" % data['cabinet_num'])
        return json.dumps({'code': 0, 'result': 'create cabinet asset success!'})
    except:
        # 捕捉异常
        utils.write_log('api').error("Create cabinet error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Create cabinet asset failed'})



'''
更新机柜的api
'''
@jsonrpc.method('cabinet.update')
def update_cabinet(*args,**kwargs):
    try:
        # 获取前端传来的数据
        data = request.get_json()['params']
        # 获取where条件
        where = data.get('where', None)
        # 获取要更新这条的数据
        data = data.get('data', None)
        # 指定输出的内容
        output = [
            'id','cabinet_num',
            'position',
            'idc_id',
            'physical',
            'switch',
            'vm'
        ]
        # 对进行传入的数据进行检查书否符合需求
        if app.config['cursor'].get_one_result('cabinet', output, {'cabinet_num': data['cabinet_num']}) and \
                        app.config['cursor'].get_one_result('cabinet', output, {'cabinet_num': data['cabinet_num']})['id'] != \
                        app.config['cursor'].get_one_result('cabinet', output, {'id': data['id']})['id']:
            return json.dumps({'code': 1, 'errmsg': "cabinet_num already is exist!"})
        for _key in 'cabinet_num,idc_id,physical,switch,vm'.split(','):
            _value = data.get(_key).strip()
            if _value == '':
                return json.dumps({'code': 1, 'errmsg': '%s Not allowed to empty!' % _key})
        for _key in 'physical,switch,vm'.split(','):
            _value = data.get(_key).strip(',')
            if not _value.isdigit():
                return json.dumps({'code': 1, 'errmsg': '%s Must be an integer!' % _key})
        # 进行更新数据
        app.config['cursor'].execute_update_sql('cabinet', data, where)
        # 写入日志
        utils.write_log('api').info("update cabinet success: %s" % data['cabinet_num'])
        return json.dumps({'code': 0, 'result': 'Update cabinet assets success!'})
    except:
        # 捕捉异常
        utils.write_log('api').error("Update cabinet error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Update cabinet failed'})



'''
删除机柜的api
'''
@jsonrpc.method('cabinet.delete')
def delete_cabinet(**kwargs):
    try:
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #进行删除
        app.config['cursor'].execute_delete_sql('cabinet',where)
        #执行记录日志
        utils.write_log('api').info("delete cabinet success")
        #进行返回
        return json.dumps({'code': 0, 'result': 'Delete cabinet success!'})
    except:
        #捕捉异常
        utils.write_log('api').error("Delete cabinet error: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'Delete cabinet failed'})



'''
查看见机房机器数量
'''
@jsonrpc.method('server.machen')
def machen_server(**kwargs):
    try:
        output = [
            'count(*)'
        ]
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #输出的相关字段
        fields = data.get('output',output)
        #进行查看
        result = app.config['cursor'].get_results('asset',fields,where)
        #执行记录日志
        utils.write_log('api').info("select server macken success")
        #进行返回
        return json.dumps({'code': 0, 'result': result})
    except:
        #捕捉异常
        utils.write_log('api').error("select server macken faild: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select server macken faild'})


'''
查看机器类型以及数量
'''
@jsonrpc.method('server.model')
def model_server(**kwargs):
    try:
        output = [
            'model_id'
        ]
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #输出的相关字段
        fields = data.get('output',output)
        #进行查看
        result = app.config['cursor'].get_results('asset',fields,where)
        _result = app.config['cursor'].get_results('model',['model','id'])
        r = dict([item.values() for item in _result])
        r = dict(zip(r.values(),r.keys()))
        id_list = [item.values()[0] for item in result]
        rs_dict = {}
        c = Counter(id_list)
        for e in c:
            if r.has_key(e):
                rs_dict[r[e]] = c[e]
        result = rs_dict
        #执行记录日志
        utils.write_log('api').info("select server model success")
        #进行返回
        return json.dumps({'code': 0, 'result': result})
    except:
        #捕捉异常
        utils.write_log('api').error("select server model faild: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select server model faild'})



'''
查看机器的规格
'''
@jsonrpc.method('server.specific')
def specific_server(**kwargs):
    try:
        output = [
            'spec_id'
        ]
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #输出的相关字段
        fields = data.get('output',output)
        #进行查看
        result = app.config['cursor'].get_results('asset',fields,where)
        _result = app.config['cursor'].get_results('spec',['spec','id'])
        r = dict([item.values() for item in _result])
        r = dict(zip(r.values(),r.keys()))
        id_list = [item.values()[0] for item in result]
        rs_dict = {}
        c = Counter(id_list)
        for e in c:
            if r.has_key(e):
                rs_dict[r[e]] = c[e]
        result = rs_dict
        #执行记录日志
        utils.write_log('api').info("select server model success")
        #进行返回
        return json.dumps({'code': 0, 'result': result})
    except:
        #捕捉异常
        utils.write_log('api').error("select server model faild: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select server model faild'})




@jsonrpc.method('server.cabinet_machen')
def server_cabinet_machen(**kwargs):
    try:
        output = [
            'cabinet_seat_id','idc_id'
        ]
        #获取前端出来的数据
        data = request.get_json()['params']
        #获取where条件
        where = data.get('where', None)
        #输出的相关字段
        fields = data.get('output',output)
        #进行查看
        result = app.config['cursor'].get_results('asset',fields,where)
        _result = app.config['cursor'].get_results('cabinet',['id','cabinet_num'])
        __result = app.config['cursor'].get_results('idc',['id','name'])
        id_list = [(item.values()[0],item.values()[1])for item in result]
        _id_list = dict([item.values() for item in _result])
        _id_list = dict(zip(_id_list.values(),_id_list.keys()))
        __id_list =dict([[item.values()[0],item.values()[1]]for item in __result])
        rs_dict = {}
        id_list = Counter(id_list)
        for item in id_list:
            if __id_list.has_key(item[0]) and _id_list.has_key(item[1]):
                key_str = '%s %s' %(__id_list[item[0]],_id_list[item[1]])
                rs_dict[key_str] = id_list[item]
        result = rs_dict
        #执行记录日志
        utils.write_log('api').info("select server model success")
        #进行返回
        return json.dumps({'code': 0, 'result': result})
    except:
        #捕捉异常
        utils.write_log('api').error("select server model faild: %s" % traceback.format_exc())
        return json.dumps({'code': 1, 'errmsg': 'select server model faild'})

