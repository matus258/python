#!/usr/bin/python3
import boto3
import json

#regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]

regions = ["us-east-1","sa-east-1"]
array= list()
regiao= list()
status=list()
r = dict()

for region in regions:
    ec2 = boto3.client('ec2',region_name=region)
    response = ec2.describe_vpn_connections()
    for vpn in response['VpnConnections']:
        for d in status:
            status.pop()
        #print(json.dumps(vpn, indent=2 , default = str))
        for vgw in vpn['VgwTelemetry']:
            #print(json.dumps(vgw.get('Status'), indent=2 , default = str))
            status.append(vgw.get('Status'))
        if vpn['VpnConnectionId'] == 'vpn-99961f84':
            status[0] = 'DOWN'
            status[1] = 'UP'     
        if status[0] == 'UP' or status[1] == 'UP':
            arrar={"VpnConnectionId": vpn['VpnConnectionId'], 'Status': 'UP' }
            #print('VpnConnectionId: $VPN$ \n Status: UP'.replace('$VPN$',vpn['VpnConnectionId']))
        else:
            r={"VpnConnectionId": vpn['VpnConnectionId'], 'Status': 'DOWN' }
            #print('VpnConnectionId: $VPN$ \n Status: DOWN'.replace('$VPN$',vpn['VpnConnectionId']))
             
print(json.dumps(r, indent =2, default =str))
