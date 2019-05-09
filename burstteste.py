#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime
regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
# for region in regions:
now = datetime.now()
if now.month == 1:
    start_time = datetime(now.year-1,now.month+11,now.day)
else:
    start_time=datetime(now.year,now.month-1,now.day)

end_time=datetime(now.year,now.month,now.day)
efs = boto3.client('efs')
response = efs.describe_file_systems()
cloudwatch = boto3.client('cloudwatch')
cont =0
for f in response.get('FileSystems'):

#print(json.dumps(response.get('FileSystems'), indent=2, default=str))
    r = cloudwatch.get_metric_data (MetricDataQueries=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EFS',
                            'MetricName': 'BurstCreditBalance',
                            'Dimensions': [
                                {
                                    'Name': 'FileSystemId',
                                    'Value': f.get('FileSystemId')
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
    print(r.get('MetricDataResults'))
    for met in r.get('MetricDataResults'):
        for val in met.get('Values'):
            cont += val
            print(cont)