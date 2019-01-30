#!/usr/bin/python3

from pyzabbix import ZabbixAPI

zapi = ZabbixAPI("http://192.168.10.186/zabbix")
zapi.login("admin", "zabbix")
hostid_antigo = 0
hostid_novo = 0
cont = 0
for i in zapi.httptest.get(output="extend"):
    hostid_novo = i['hostid']
    if hostid_novo != hostid_antigo:
        hostid_antigo = hostid_novo
        cont += 1
    
print(cont)

    
    