#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime

em_uso =list()
nao_uso = list()
now = datetime.now()
cont = 0
regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
res = dict()
regiao = list()
qnt_reg = 0


if now.month == 1:
    start_time = datetime(now.year-1,now.month+11,now.day)
else:
    start_time=datetime(now.year,now.month-1,now.day)

end_time=datetime(now.year,now.month,now.day)

for region in regions:
    cloudwatch = boto3.client('cloudwatch',region_name=region)
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
                        'Period': 300,
                        'Stat': 'Sum',
                        'Unit': 'Bytes'
                    },
                
                },
            ],
            
            StartTime=start_time,
            EndTime=end_time,
            ScanBy='TimestampDescending',
            MaxDatapoints=123)

        for met in r.get('MetricDataResults'):
            for val in met.get('Values'):
                if val > 0:
                    cont += 1

        if cont > 0:
            res[vpn] = True # print('$VPNID$ : VPN em uso'.replace('$VPNID$', vpn))
            em_uso.append(vpn)
        else:
            res[vpn] = False # print('$VPNID$ : VPN não está em uso'.replace('$VPNID$', vpn))
            nao_uso.append(vpn)
        regiao.append(region)    

#print(json.dumps(res, indent=2, sort_keys=True))

unidade='c'
diretorioBase=''

if os.name == 'nt':
    diretorioBase=unidade+':'
else:
    diretorioBase=os.getenv("HOME")
caminhoAbsoluto = diretorioBase + os.sep + 'csv' + os.sep
if not os.path.exists(caminhoAbsoluto):
    os.makedirs(caminhoAbsoluto)

arquivoOutput = caminhoAbsoluto + 'Verificar VPNS.csv'

with open(arquivoOutput, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['VpnID','Região', 'Estado'])

    for i in em_uso:
        spamwriter.writerow([i,regiao[qnt_reg], 'Em uso'])
        qnt_reg += 1
    for n in nao_uso:
        spamwriter.writerow([n,regiao[qnt_reg], 'Fora de uso'])
        qnt_reg += 1

print('Arquivo gerado no diretorio: ' + arquivoOutput)        