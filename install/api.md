## 资产平台api  ##

实例:

	post/api:
	
	{
	“comtent-type”:”application/json”,
	“content-length”:”113”
	“server”:”Werkzeug/0.8.3 Python/2.7.5”,
	“data” :{
	“jsonrpc”:”2.0”,   >> jsonrpc版本号必须打上,否则会报错.
	“id”:”1”,
	“method”:”Api.welcome”,>>查看idc列表的模块加上方法
	“params”:[]  >>接口接受的参数和数据
	
			}
	}


	Response:

	
	{
	 “id”:”1”
	 “jsonrpc”:”2.0”,
	 “result”:”welcome to flask JSON-RPC”
	}


一、资产查看

	data = {
        'jsonrpc':2.0,  
        'method':"asset.list", 
        'id':"1",
        'params':{
            'where':{"status":0} 
        }

二、资产创建:
	
	data = {
        'jsonrpc':2.0,
        'method':"asset.create",
        'id':"1",
        'params':{
            'sn':'xxxxxi',
            'inner_ip':'192.168.6.5',
            'app_ip':'192.168.3.6',
            'remote_ip':'192.168.3.7',
            'mac':'kk:ll:dd:ww:xx',
            'hostname':'hhjh',
            'os':'centos6',
            'cpu':'2核/64',
            'nu_ram':'6',
            'nu_disk':'4',
            'ram':'2048',
            'disk':'500',
            'idc_id':'2',
            'raid':'10',
            'raid_type':'kk_xx',
            'admin':'lbb',
            'business':'a站',
            'remote_card':'hhh',
            'purchase_date':'1978-11-11',
            'warranty':'1989-11-11',
            'vendor':'dell',
            'model':'r710',
            'remark':'ooo',
            'status':0
        }
	
三、资产更新

	data = {
    'jsonrpc': 2.0,
    'method': "asset.update,
    'id': "1",
    'params': {
            sn':'xxxxxi',
            'inner_ip':'192.168.6.5',
            'app_ip':'192.168.3.6',
            'remote_ip':'192.168.3.7',
            'where':{"status":0,”id”:3}
    }


四、资产删除
	
	 data = {
     'jsonrpc': 2.0,
     'method': "asset.delete",
     'id': "1",
     'params': {
             'where':{'id':8}
     }


上述为资产的api实例

如下IDC：

	-idc.list >>查看
	-idc.create >>创建
	-idc.update >>更新
	-idc.delete >> 删除


如下机柜:
	
	-cabinet.list >>查看
	-cabinet.create >>创建
	-cabinet.update >>更新
	-cabinet.delete >>删除

如下虚拟机:
	
	-vm.list  >>查看
	-vm.create >>创建
	-vm.update >>更新
	-vm.delete >>删除	