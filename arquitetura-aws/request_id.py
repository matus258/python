#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import boto3
import json
import os
import csv
from datetime import datetime


regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
#regions = ["us-east-1", "sa-east-1"]
regiao= list()
status = list()
instancias = list()
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
url = os.environ.get("ZABBIX_URL")
user= os.environ.get("ZABBIX_USER")
senha = os.environ.get("ZABBIX_PASS")
zapi=ZabbixAPI('http://monit.techne.com.br/zabbix/')
zapi.login('Admin','elfos123')
name = ''

import boto3
from operator import itemgetter

client = boto3.client('ec2')
response = client.describe_images(Filters=[{'Name'},])
print(json.dumps(response,indent=2, default=str))