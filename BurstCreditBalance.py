#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime

regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
res = list()
regiao = list()
qnt_reg = 0
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
ins_type =list()

if now.month == 1:
    start_time = datetime(now.year-1,now.month+11,now.day)
else:
    start_time=datetime(now.year,now.month-1,now.day)

end_time=datetime(now.year,now.month,now.day)
for region in regions:
    type_cont=0
    ec2 = boto3.client('ec2',region_name=region)
    resp = ec2.describe_instances()
    cloudwatch = boto3.client('cloudwatch',region_name=region)
    response = cloudwatch.list_metrics(Namespace='AWS/EC2', MetricName='CPUCreditUsage')
    instance_id = list()
    for met in response['Metrics']:
        for dim in met.get('Dimensions'):
                for res_ins in resp['Reservations']:
                    for ins in res_ins['Instances']:
                        if dim['Value'] == ins['InstanceId']:
                            ins_type.append(ins['InstanceType'])
                            instance_id.append(dim['Value'])
    
    for ec2 in instance_id:
        cont =0
        r = cloudwatch.get_metric_data (MetricDataQueries=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUCreditUsage',
                            'Dimensions': [
                                {
                                    'Name': 'InstanceId',
                                    'Value': ec2
                                },
                            ]
                        },
                        'Period': 2592000,
                        'Stat': 'Sum',
                        'Unit': 'Count'
                    },
                
                },
            ],
            
            StartTime=start_time,
            EndTime=end_time,
            ScanBy='TimestampDescending')

        for met in r.get('MetricDataResults'):
            for val in met.get('Values'):
                cont += val
        if ins_type[type_cont] == 't2.nano':
            credit_gan = 2160
        elif ins_type[type_cont] == 't2.micro':
            credit_gan = 4320
        elif ins_type[type_cont] == 't2.small':
            credit_gan = 8640                
        elif ins_type[type_cont] == 't2.medium':
            credit_gan = 17280
        elif ins_type[type_cont] == 't2.large':
            credit_gan = 25920
        elif ins_type[type_cont] == 't2.xlarge':
            credit_gan = 38880
        elif ins_type[type_cont] == 't2.2xlarge':
            credit_gan = 58752
        elif ins_type[type_cont] == 't3.nano':
            credit_gan = 4320        
        elif ins_type[type_cont] == 't3.micro':
            credit_gan = 8640
        elif ins_type[type_cont] == 't3.small':
            credit_gan = 17280
        elif ins_type[type_cont] == 't3.medium':
            credit_gan = 17280            
        elif ins_type[type_cont] == 't3.large':
            credit_gan = 25920
        elif ins_type[type_cont] == 't3.xlarge':
            credit_gan = 69120
        elif ins_type[type_cont] == 't3.2xlarge':
            credit_gan = 138240


        porcent = (cont / credit_gan)*100
        if porcent <= 20 or porcent >= 85:
            res.append({'InstanceType': ins_type[type_cont],
                'InstanceId': ec2,
                'Region': region,
                'Creditos usados': round(cont, 2),
                'Creditos ganhos': credit_gan,
                'Porcentagem de uso': '$POR$ %'.replace('$POR$', str(round(porcent, 2))) })
        type_cont += 1