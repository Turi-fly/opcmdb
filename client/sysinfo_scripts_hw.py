#!/usr/bin/python
#coding:utf-8
#物理机信息


import socket #导入socket 用来获取主机名
import psutil #导入psutil工具
import subprocess
import re
import time
import platform
import requests
import json


device_white = ["br0","em1","br_em1","cloudbr0","eth0"]

def get_hostname():
    return socket.gethostname()

def get_meminfo():
    mem = None
    with open("/proc/meminfo") as f:
        for line in f:
            if "MemTotal" in line:
                mem = int(line.split()[1])
                break
    return mem / 1024

def get_device_info():
    ret = []
    for device,info in psutil.net_if_addrs().items():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address #ip
                if snic.family == 17:
                    device_info['mac'] = snic.address #mac
            ret.append(device_info)
    return ret

def get_cpuinfo():
    ret = {"cpu":'',"num":0}
    with open("/proc/cpuinfo") as f:
        for line in f:
            tmp = line.strip().split(":")
            key = tmp[0].rstrip()
            if key == "model name":
                ret['cpu'] = tmp[1].lstrip()
            elif key == "processor":
                ret["num"] += 1
    return ret

def get_disk():
    #dev_white = ['sda','sdb','sdc']
    ret = []
    #cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    cmd = """/sbin/parted -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for dev in disk_data.stdout.readlines():
        if "sda" in dev:
	    size = dev.strip().split(':')[1].strip()[:-2]
            ret.append(str(size))
    return " + ".join(ret)

#获取制造商
def get_manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        if "Manufacturer" in line:
            if 'Dell' in line.split(":")[1].strip():
		ret['type_id'] = 1
            if 'Hp' in line.split(":")[1].strip():
		ret['type_id'] = 2
            #print line.split(":")[1].strip()
        elif "Product Name" in line:
            if 'R730xd' in line.split(":")[1].strip():
		ret['model_id'] = '1'
	    if 'R720xd' in line.split(":")[1].strip():
    		ret['model_id'] = '2'                    
	    if 'R630' in line.split(":")[1].strip():
    		ret['model_id'] = '3'                    
	    if 'R620' in line.split(":")[1].strip():
    		ret['model_id'] = '4'                    
	    if 'R430' in line.split(":")[1].strip():
    		ret['model_id'] = '5'                    
	    if 'R420' in line.split(":")[1].strip():
    		ret['model_id'] = '6'                    
	    if 'R410' in line.split(":")[1].strip():
    		ret['model_id'] = '7'                    
	    if 'R730' in line.split(":")[1].strip():
    		ret['model_id'] = '8'                    
            #print line.split(':')[1].strip()
        elif "Serial Number" in line:
            ret['sn'] = line.split(':')[1].strip().replace(' ','')
            #print line.split(':')[1].strip().replace(' ','')
    return ret

#获取出厂日期
def get_rel_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    date = data.stdout.readline().split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',date)


#获取内存个数
def get_num_ram():
    cmd = """dmidecode -t memory|grep Size | egrep -v "No Module Installed" | wc -l"""
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return data.stdout.readline().strip()

#获取规格信息
def get_spec():
    cmd = """dmidecode -t 3|grep 'Height'|awk -F ':' '{print $2}' | awk '{print $1}'"""
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return data.stdout.readline().strip()

#获取cpu的个数
def get_nu_cpu():
    cmd = """grep "physical id" /proc/cpuinfo |sort -u|wc -l"""
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return data.stdout.readline().strip()

#获取内存的版本号
def get_os_version():
    return " ".join(platform.linux_distribution())


def get_innerIp(ipinfo):
    inner_device = ["eth1","bond0"]
    ret = {}
    for info in ipinfo:
        if info.has_key('ip') and info.get('device',None) in inner_device:
            ret['inner_ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return ret
    return {}

def get_raid():
    cmd_pri = "MegaCli -LDInfo -Lall -aALL | grep RAID | awk -F '[:,-]' NR==1'{print $3}'"
    cmd_sec = "MegaCli -LDInfo -Lall -aALL | grep RAID | awk -F '[:,-]' 'NR==1{print $5}'"
    cmd_d = "MegaCli -cfgdsply -aALL | grep '^Number Of Drives'|sort -u | awk -F '[:]' 'NR==1{print $2}'"
    cmd_e = "MegaCli -cfgdsply -aALL | grep '^Span Depth'|sort -u | awk  'NR==1{print $NF}'"
    data_pri = subprocess.Popen(cmd_pri,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    data_sec = subprocess.Popen(cmd_sec,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    data_d = subprocess.Popen(cmd_d,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    data_e = subprocess.Popen(cmd_e,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    raid_level=str(data_pri.stdout.readline().strip())+str(data_sec.stdout.readline().strip())
    d_if = str(data_d.stdout.readline().strip())
    e_if = str(data_e.stdout.readline().strip())
    print data_d,data_e,raid_level,d_if,e_if
    if raid_level == '00':
        raid_id = 1
    elif raid_level == '10' and d_if == '2' and e_if == '1':
        raid_id = 2
    elif raid_level == '10' and d_if == '1' and e_if == '1':
        raid_id = 2
    elif raid_level == '10' and d_if == '4' or d_if == '2' or e_if != '1':
        raid_id = 4
    elif raid_level == '50':
        raid_id = 3
    elif raid_level == '13':
        raid_id = 4
    return raid_id

def get_num_disk():
    cmd = '''MegaCli -LdPdInfo -aAll -NoLog | grep Slot | wc -l'''
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    num_disk = data.stdout.readline().strip()
    return num_disk

def get_disk_type():
    cmd = "MegaCli -LdPdInfo -aAll -NoLog | grep PD | grep Type | awk -F '[:]' 'NR==1{print $2}'"
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    disk_type = data.stdout.readline().strip()
    return disk_type

def get_raid_type():
    cmd = "MegaCli -cfgdsply -aALL | grep Product |awk -F '[:]' '{print $2}'"
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    raid_type = data.stdout.readline().strip()
    return raid_type

def get_slot_mem():
    cmd = "dmidecode --type memory | grep 'Memory Device' |wc -l"
    data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    slot_ram = data.stdout.readline().strip()
    return slot_ram
    

def run():
    data = {}
    data['hostname'] = get_hostname()
    device_info = get_device_info()
    for device in device_info:
	if device.has_key('ip'):
		ip = device['ip']
    data['inner_ip'] = ip
    #data.update(get_innerIp(device_info))
    #data['ipinfo'] = json.dumps(device_info)
    cpuinfo = get_cpuinfo()
    data['cpu'] = "{num}核/{cpu}".format(**cpuinfo)
    data['disk'] = '%s' % get_disk()             
    data['ram'] = '%s' % get_meminfo()           
    data.update(get_manufacturer())
    data['purchase_date'] = get_rel_date()
    data['os'] = get_os_version()
    data['spec_id'] = get_spec()
    data['nu_ram'] = get_num_ram()
    data['raid_id'] = get_raid()
    data['nu_disk'] = get_num_disk()
    data['disk_type'] = get_disk_type()
    data['raid_type'] = get_raid_type()
    data['slot_ram']  = get_slot_mem()
    data['nu_cpu']    = get_nu_cpu()
    return send(data)
    #print data
def send(data):
    headers = {'content-type':'application/json'}   
    url = "http://192.168.0.196:1000/api"           
    data = {                                        
        'jsonrpc':2.0,                          
        'method':"asset.create",                   
        'id':"1",                               
        'params':data                           
            }                                   
    r = requests.post(url,headers=headers,json=data)
    return r.text                                   


if __name__ == "__main__":
    print run()
