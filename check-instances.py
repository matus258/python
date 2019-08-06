#!/usr/bin/python3
import boto3
import json
import os
import csv
import sys
import getopt
from datetime import datetime
from os import environ

try:
    opts, args = getopt.getopt(sys.argv[1:],"ha:s:",["akid=","secret="])
except Exception as e:
    print(e)
    sys.exit(1)
for opt, arg in opts:
    if opt == '-h':
environ['AWS_ROLE_NAME']=
environ['AWS_SESSION_NAME']=

accounts = []

regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
#regions = ["us-east-1", "sa-east-1"]
alias = ''
regiao= list()
status = list()
instancias = list()
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key=''
)
def role_arn_to_session(arn_id,session):
    client = session.client('sts')
    response = client.assume_role(
        RoleArn="arn:aws:iam::"+arn_id+":role/"+environ['AWS_ROLE_NAME'],
        RoleSessionName=environ['AWS_SESSION_NAME']
    )
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken']
    )
for arn_id in accounts:
    print('\n'+arn_id)
    role = role_arn_to_session(arn_id, session)
    for region in regions:
        print('\n'+region)
        ec2 = role.client('ec2', region_name=region)
        response = ec2.describe_instances()
        for r in response['Reservations']:
            for instance in r['Instances']:
                if instance['State'].get('Name') == 'running':
                    for tag in instance.get('Tags',[]):
                        if tag['Key'] == 'Name':
                            name=tag['Value']
                    publicip=''
                    keyname=instance.get('KeyName','')
                    privateip=instance.get('PrivateIpAddress','')
                    try:
                        img=ec2.describe_images(ImageIds=[imgid])['Images'][0]
                    except:
                        img={}
                    for network in instance['NetworkInterfaces']:
                        pubip=network.get('Association',{}).get('PublicIp')
                        if pubip:
                            publicip = pubip
                            break
                
                        
                    result={
                        "Region": region,
                        "AccountNumber": arn_id,
                        "Alias": alias,
                        "Name": name,
                        "PrivateIpAddress": privateip
                    }
                    instancias.append(result)
                    print('.', end='')
print(json.dumps(instancias,indent=4,default=str))
regiao.append(region)  

unidade='c'
diretorioBase=''

if os.name == 'nt':
    diretorioBase=unidade+':'
else:
    diretorioBase=os.getenv("HOME")
caminhoAbsoluto = diretorioBase + os.sep + 'csv' + os.sep
if not os.path.exists(caminhoAbsoluto):
    os.makedirs(caminhoAbsoluto)

arquivoOutput = caminhoAbsoluto + 'Lista de instancias $DATA$.csv'.replace('$DATA$', date)

with open(arquivoOutput, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Region','AccountNumber','Alias','Name','PrivateIpAddress'])
    for i in instancias:
        spamwriter.writerow([i['Region'],i['AccountNumber'],i['Alias'],i['Name'],i['PrivateIpAddress']])
print('Arquivo gerado no diretorio: ' + arquivoOutput)        
