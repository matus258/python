#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import os
import boto3

# informaçoes do zabbix server
url = os.environ.get("ZABBIX_URL")
user= os.environ.get("ZABBIX_USER")
senha = os.environ.get("ZABBIX_PASS")
zapi=ZabbixAPI(url)
zapi.login(user, senha)

for h in zapi.host.get(output=["dns", "ip", "useip"], selectHosts=["host"], filter={"main": 1, "type": 1}):
    # Make sure the hosts are named according to their FQDN
    if h['dns'] != h['hosts'][0]['host']:
        print('Warning: %s has dns "%s"' % (h['hosts'][0]['host'], h['dns']))

