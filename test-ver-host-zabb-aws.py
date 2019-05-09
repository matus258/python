#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import os
import boto3
import boto3
import json


ec2 = boto3.client('ec2')
response = ec2.describe_instances()
# informaçoes do zabbix server
url = os.environ.get("ZABBIX_URL")
user= os.environ.get("ZABBIX_USER")
senha = os.environ.get("ZABBIX_PASS")
zapi=ZabbixAPI('http://monit.techne.com.br/zabbix/')
zapi.login('Admin', 'elfos123')


for zab in zapi.host.get():
    print(zab['host'])
    # for aws in response.get('Reservations').get('Instances').get('Tags')[1].get('Value'):
    #     print(aws)
