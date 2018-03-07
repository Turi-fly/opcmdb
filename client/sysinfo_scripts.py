#!/usr/bin/python
#coding:utf-8


import socket #导入socket 用来获取主机名
import psutil #导入psutil工具
import subprocess
import re
import time
import platform
import requests
import json


device_white = ["eth0"]


#收集系统主机名
def get_hostname():
    return socket.gethostname()

#收集系统内存信息
def get_meminfo():
    mem = None
    with open("/proc/meminfo") as f:
        for line in f:
            if "MemTotal" in line:
                mem = int(line.split()[1])
                break
    return mem / 1024

#收集系统网卡信息和mac地址信息
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

#收集系统cpu信息
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
    cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for dev in disk_data.stdout.readlines():
        if "vda" in dev:
            size = int(dev.strip().split(",")[1].split()[0]) / 1024 / 1024 / 1024
            ret.append(str(size))
    return " + ".join(ret)

def get_manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        if "UUID" in line:
            ret['uuid'] = line.split(':')[1].strip()
    return ret

def get_innerIp(ipinfo):
    inner_device = ["eth1","bond0"]
    ret = {}
    for info in ipinfo:
        if info.has_key('ip') and info.get('device',None) in inner_device:
            ret['inner_ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return ret
    return {}


def run():
    data = {}
    data['vm'] = get_hostname()
    device_info = get_device_info()
    data['mac'] = "%s/%s" %(device_info[0]['device'],device_info[0]['mac'])
    data['ip'] = device_info[0]['ip']
    #data['ipinfo'] = json.dumps(device_info)
    cpuinfo = get_cpuinfo()
    data['cpu'] = "{cpu}/{num}".format(**cpuinfo)
    data['disk'] = '%s' % get_disk()
    data['ram'] = '%s' % get_meminfo()
    data.update(get_manufacturer())
    return send(data)

def send(data):
    headers = {'content-type':'application/json'}
    url = "http://192.168.200.75:8080/api"
    data = {
	    'jsonrpc':2.0,
            'method':"vm.create",
            'id':"1",	
	    'params':data
		}
    r = requests.post(url,headers=headers,json=data)
    return r.text



if __name__ == "__main__":
    print run()
