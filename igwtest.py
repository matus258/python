#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime


regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
regiao_em_uso=list()
regiao_nao_uso=list()
qnt_reg_em_uso = 0
qnt_reg_nao_uso = 0
em_uso= list()
nao_uso=list()
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
res=dict()

for region in regions:
    ec2 = boto3.client('ec2',region_name=region)
    response = ec2.describe_internet_gateways()
    for inter_gat in response.get('InternetGateways'):
        print()
        if not inter_gat.get('Attachments'):
            #res[inter_gat.get('InternetGatewayId')]= 'Fora de Uso'
            nao_uso.append(inter_gat.get('InternetGatewayId'))
            regiao_nao_uso.append(region)
            continue
        for vpc in inter_gat.get('Attachments'):
            if vpc['VpcId']:
                #res[inter_gat.get('InternetGatewayId')]= 'Em uso'
                em_uso.append(inter_gat.get('InternetGatewayId'))
            regiao_em_uso.append(region)