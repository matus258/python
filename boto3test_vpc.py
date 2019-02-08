#!/usr/bin/python3

import boto3
import json
 
ec2 = boto3.client('ec2')
resp = ec2.describe_instances()
response = ec2.describe_internet_gateways()
#print(json.dumps(response.get('InternetGateways'), indent=2))
#for inter_gat in response.get('InternetGateways'):
    #print(json.dumps(inter_gat, indent=2))
    #print(json.dumps(inter_gat.get('InternetGatewayId'), indent=2))
    #for vpc in inter_gat.get('Attachments'):
        #print(json.dumps(vpc['VpcId'], indent=2))
for aws in resp.get('Reservations').get('Instances')[0]:
        print(aws)