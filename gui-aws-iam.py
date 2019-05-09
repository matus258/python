#!/usr/bin/python3

import boto3
import json
import csv
import os

iam = boto3.client('iam')
resp = iam.list_users()
result = list()
pol=list()

for users in resp['Users']:
    user=users['UserName']

    response = iam.list_attached_user_policies(
    UserName=user)
    group=iam.list_groups_for_user(UserName= user)
    for g in group['Groups']:
        gp = g['GroupName']
        re = iam.list_attached_group_policies(GroupName=gp)
        for pog in re['AttachedPolicies']:
            result.append({'UserName': user,
                        'Anexado': 'A partir do grupo',
                        'GroupName': gp,
                        'PolicyName': pog.get('PolicyName') })

    for po in response['AttachedPolicies']:
        result.append({'UserName': user,
                    'Anexado': 'Diretamente',
                    'PolicyName': po.get('PolicyName') })    


unidade='c'
diretorioBase=''

if os.name == 'nt':
    diretorioBase=unidade+':'
else:
    diretorioBase=os.getenv("HOME")
caminhoAbsoluto = diretorioBase + os.sep + 'csv' + os.sep
if not os.path.exists(caminhoAbsoluto):
    os.makedirs(caminhoAbsoluto)

arquivoOutput = caminhoAbsoluto + 'Relatorio-de-usuarios.csv'

with open(arquivoOutput, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['UserName','Anexado', 'GroupName','PolicyName'])

    for u in result:
        spamwriter.writerow([u['UserName'],u['Anexado'],u.get('GroupName',None),u['PolicyName']])


print('Arquivo gerado no diretorio: ' + arquivoOutput)  
# print(json.dumps(result, indent=2, default=str))
