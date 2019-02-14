import json
import boto3
import csv
import os
from datetime import datetime
from general.lambda_utils import *

def check_vpn(session):
    now = datetime.now()
    cont = 0
    regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
    res = dict()
    
    if now.month == 1:
        start_time = datetime(now.year-1,now.month+11,now.day)
    else:
        start_time=datetime(now.year,now.month-1,now.day)
    
    end_time=datetime(now.year,now.month,now.day)
    
    for region in regions:
        cloudwatch = session.client('cloudwatch',region_name=region)
        response = cloudwatch.list_metrics(Namespace='AWS/VPN', MetricName='TunnelDataIn')
        vpnid = list()
        for met in response['Metrics']:
            for dim in met.get('Dimensions'):
                if dim['Name'] == 'VpnId':
                    vpnid.append(dim['Value'])
        for vpn in vpnid:
            cont =0
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
                                        'Value': vpn
                                    },
                                ]
                            },
                            'Period': 2592000,
                            'Stat': 'Sum',
                            'Unit': 'Bytes'
                        },
                    
                    },
                ],
                
                StartTime=start_time,
                EndTime=end_time,
                ScanBy='TimestampDescending')
    
            for met in r.get('MetricDataResults'):
                for val in met.get('Values'):
                    if val > 0:
                        cont += 1
    
            if cont > 0:
                res[vpn] = True # print('$VPNID$ : VPN em uso'.replace('$VPNID$', vpn))
                
            else:
                res[vpn] = False # print('$VPNID$ : VPN não está em uso'.replace('$VPNID$', vpn))
    return res

def lambda_handler(event, context):
    params = verify_parameters(event, {
        'akid': None, 'aksecret': None, 'alias': None
    })
    result = dict()
    session = False
    if params.get('akid') and params.get('aksecret'):
        session = boto3.Session(
            aws_access_key_id=params['akid'],
            aws_secret_access_key=params['aksecret']
        )
    if(session):
        if params['alias']:
            session = switch_role(params['alias'],session)
            vpns = check_vpn(session) # executa sua parte
            return final_response(200, vpns)
    else:
        result['error'] = "Account Inaccessible"
    return final_response(200, result)