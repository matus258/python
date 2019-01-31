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
zapi=ZabbixAPI(url)
zapi.login(user, senha)


res_tam = len(response.get('Reservations'))
cont=0
name = list()

for zab in zapi.host.get():

    for i in range(res_tam):
        ins_tam =len(response.get('Reservations')[i].get('Instances'))
        for ins in range(ins_tam):

            #print(json.dumps(response.get('Reservations')[i].get('Instances')[ins].get('Tags'), indent=2, default=str))
            tag_tam = len(response.get('Reservations')[i].get('Instances')[ins].get('Tags'))
            for tag in range(tag_tam):
                key=response.get('Reservations')[i].get('Instances')[ins].get('Tags')[tag].get('Key')

                if key=="Name":
                    name.insert(cont, response.get('Reservations')[i].get('Instances')[ins].get('Tags')[tag].get('Value'))
                    if zab['host'] == name[cont]:
                        print(name[cont])  
                    cont += 1
                            

