#!/usr/bin/python3

import os
import boto3
import json


ec2 = boto3.client('ec2')
response = ec2.describe_instances()

ip = input("Digite o ip: ")
ips = ip.split()

for i in ips:
    for res in response['Reservations']:
        for ins in res['Instances']:
            for net in ins['NetworkInterfaces']:
                if net.get('PrivateIpAddress') == i:
                    if ins.get('Tags'):
                        for tag in ins['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                    print("IP: $IP$ contem na aws \n Tag: $TAG$ ".replace('$IP$',i).replace('$TAG$', name))
                               
                    