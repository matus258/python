import json
import boto3
import csv
import os
from datetime import datetime
from general.lambda_utils import *

def check_igw(session):
    regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
    res=dict()
    for region in regions:
        ec2 = session.client('ec2',region_name=region)
        response = ec2.describe_internet_gateways()
        for inter_gat in response.get('InternetGateways'):
            if not inter_gat.get('Attachments'):
                res[inter_gat.get('InternetGatewayId')]= 'Fora de Uso'
                #regiao_nao_uso.append(region)
                continue
            for vpc in inter_gat.get('Attachments'):
                if vpc['VpcId']:
                    res[inter_gat.get('InternetGatewayId')]= 'Em uso'
                #regiao_em_uso.append(region)
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
            igws = check_igw(session) # executa sua parte
            return final_response(200, igws)
    else:
        result['error'] = "Account Inaccessible"
    return final_response(200, result)    