#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime
from general.lambda_utils import *

def check_ec2_reserved(session):
    regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
    now = datetime.now()
    date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
    if now.month == 1:
        data_mes = datetime(now.year-1,now.month+11,now.day)
    else:
        data_mes=datetime(now.year,now.month-1,now.day)
    res = list()

    for region in regions:
        reserverd = session.client('ec2',region_name=region)
        response = reserverd.describe_reserved_instances()
        #print(json.dumps(response['ReservedInstances'], indent=2, default=str))
        for res_ins in response['ReservedInstances']:
            #print(json.dumps(res_ins.get('End'), indent=2, default=str))
            d = datetime.strftime(res_ins.get('End'), '%d/%m/%y')
            date_end = datetime.strptime(d ,'%d/%m/%y' )
            if date_end < now and date_end > data_mes:
                res.append({'InstanceType': res_ins.get('InstanceType'),'Region': region,'Status': 'Expirada','Date': d })
            if date_end > now:
                res.append({'InstanceType': res_ins.get('InstanceType'),'Region': region,'Status': 'A expirar','Date': d })
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
            ec2_reserv = check_ec2_reserved(session) # executa sua parte
            return final_response(200, ec2_reserv)
    else:
        result['error'] = "Account Inaccessible"
    return final_response(200, result) 