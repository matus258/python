#!/usr/bin/python3

import boto3
import json
from datetime import datetime
# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

r = cloudwatch.get_metric_data (MetricDataQueries=[
        {
            'Id': 'string',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/VPN',
                    'MetricName': 'TunnelDataIn',
                    'Dimensions': [
                        {
                            'Name': 'VpnId',
                            'Value': 'vpn-99961f84'
                        },
                    ]
                },
                'Period': 300,
                'Stat': 'Sum',
                'Unit': 'Bytes'
            },
            
        },
    ],
    StartTime=datetime(2019,1,1),
    EndTime=datetime(2019,2,1),
    ScanBy='TimestampDescending',
    MaxDatapoints=123)
cont = 0
for met in r.get('MetricDataResults'):
    for val in met.get('Values'):
        if val > 0:
            cont += 1

if cont > 0:
    print('VPN em uso')