#!/usr/bin/python3

from pyzabbix import ZabbixAPI

zapi = ZabbixAPI("http://192.168.10.186/zabbix")
zapi.login("admin", "zabbix")
print("Connected to Zabbix API Version %s" % zapi.api_version())

for h in zapi.host.get(output="extend"):
    print(h['hostid'])