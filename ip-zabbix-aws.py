#!/usr/bin/python3

from pyzabbix import ZabbixAPI
import os
import boto3
import json


ec2 = boto3.client('ec2')
response = ec2.describe_instances()
# informaçoes do zabbix server
url = os.environ.get("ZABBIX_URL")
user= os.environ.get("ZABBIX_USER")
senha = os.environ.get("ZABBIX_PASS")
zapi=ZabbixAPI(url)
zapi.login(user, senha)

# Pegando o tamanho da lista Reservations
res_tam = len(response.get('Reservations'))
# Passar por cada Reservation
for res in range(res_tam):
    # Pegando o tamanho da Lista de instancias
    ins_tam =len(response.get('Reservations')[res].get('Instances'))
    # Passar por cada Instancia
    for ins in range(ins_tam):
        # Pegando o tamanho da lista NetworkInterfaces
        net_tam = len(response.get('Reservations')[res].get('Instances')[ins].get('NetworkInterfaces'))
        # Fazaendo uma condição para ignorar as instancias que não tem nada na lista NetworkInterfaces
        if net_tam != 0:
            # Passar por cada hostinterface do zabbix
            for zab in zapi.hostinterface.get():
                # Guardar o ip do host
                ip_zab = zab['ip']
                # Guardar o ip da ec2 da aws
                ip_aws=response.get('Reservations')[res].get('Instances')[ins].get('NetworkInterfaces')[0].get('PrivateIpAddress')
                # Se o ip da aws for igual ao do zabbix; retornar o ip
                if ip_aws == ip_zab:
                    print(ip_aws)
            