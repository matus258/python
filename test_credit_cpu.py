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
    ec2 = boto3.client('ec2',region_name=region)
    resp = ec2.describe_instances()
    cloudwatch = boto3.client('cloudwatch',region_name=region)
    response = cloudwatch.list_metrics(Namespace='AWS/EC2', MetricName='CPUCreditUsage')
    instance_id = list()
    for met in response['Metrics']:
        for dim in met.get('Dimensions'):
            if dim['Name'] == 'InstanceId':
                instance_id.append(dim['Value'])
                for res_ins in resp['Reservations']:
                    for ins in res_ins['Instances']:
                        if dim['Value'] == ins['InstanceId']:
                            ins_type.append(ins['InstanceType'])
    type_tam = len(ins_type)
    type_cont = 0
    for ec2 in instance_id:
        cont =0
        resp_stat = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUCreditUsage',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': ec2
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=[
                'Sum',
            ],
            Unit= 'Count'
        )

        for met in resp_stat.get('Datapoints'):
            print(met[])
        #if ins_type[type_cont] == 't2.nano':
        porcent = (cont / 2160)*100
        res.append({'InstanceType': ins_type[type_cont],
            'InstanceId': ec2,
            'Creditos usados': cont,
            'Creditos ganhos': '2160',
            'Porcentagem de uso': '$POR$ %'.replace('$POR$', str(porcent)) })