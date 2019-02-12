#!/usr/bin/python3

import boto3
import json
import csv
import os
from datetime import datetime

regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
now = datetime.now()
date =datetime(now.year,now.month,now.day).strftime('%Y-%m-%d')
if now.month == 1:
    data_mes = datetime(now.year-1,now.month+11,now.day)
else:
    data_mes=datetime(now.year,now.month-1,now.day)

expirada = list()
expirada_data = list()
aexpirar =list()
aexpirar_data =list()
regiao_expirada=list()
regiao_aexpirar=list()
qnt_reg_expirada = 0
qnt_reg_aexpirar = 0
qnt_exp =0
qnt_aexp=0


for region in regions:
    reserverd = boto3.client('ec2',region_name=region)
    response = reserverd.describe_reserved_instances()
    #print(json.dumps(response['ReservedInstances'], indent=2, default=str))
    for res_ins in response['ReservedInstances']:
        #print(json.dumps(res_ins.get('End'), indent=2, default=str))
        d = datetime.strftime(res_ins.get('End'), '%d/%m/%y')
        date_end = datetime.strptime(d ,'%d/%m/%y' )
        if date_end < now and date_end > data_mes:
            
            expirada.append(res_ins.get('InstanceType'))
            expirada_data.append(d)
            regiao_expirada.append(region)
        if date_end > now:
            aexpirar.append(res_ins.get('InstanceType'))
            aexpirar_data.append(d)
            regiao_aexpirar.append(region)
#print(json.dumps(l, indent=2, default=str))    

unidade='c'
diretorioBase=''

if os.name == 'nt':
    diretorioBase=unidade+':'
else:
    diretorioBase=os.getenv("HOME")
caminhoAbsoluto = diretorioBase + os.sep + 'csv' + os.sep
if not os.path.exists(caminhoAbsoluto):
    os.makedirs(caminhoAbsoluto)

arquivoOutput = caminhoAbsoluto + 'Check_ec2-reserved $DATA$.csv'.replace('$DATA$', date )

with open(arquivoOutput, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['InstanceType','Region', 'Status', 'Data'])

    for i in expirada:
        spamwriter.writerow([i,regiao_expirada[qnt_reg_expirada], 'Expirada', expirada_data[qnt_exp]])
        qnt_reg_expirada += 1
        qnt_exp += 1
        
    for n in aexpirar:
        spamwriter.writerow([n,regiao_aexpirar[qnt_reg_aexpirar], 'A expirar', aexpirar_data[qnt_aexp] ])
        qnt_reg_aexpirar += 1
        qnt_aexp += 1

print('Arquivo gerado no diretorio: ' + arquivoOutput)        
