#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import os

# informaçoes do zabbix server
url = os.environ.get("ZABBIX_URL")
user= os.environ.get("ZABBIX_USER")
senha = os.environ.get("ZABBIX_PASS")

zapi = ZabbixAPI(url)
zapi.login(user, senha)

for i in zapi.host.get(output= 'extend'):
    print(i['status'], type(i['status']))
    if i['status'] == '1' :
        zapi.host.delete(i['hostid'])





