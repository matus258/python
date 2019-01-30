#!/usr/bin/python3

from pyzabbix import ZabbixAPI
# informaçoes do zabbix server
zapi = ZabbixAPI("http://192.168.10.186/zabbix")
zapi.login("admin", "zabbix")

# dominios que quero adicionar
DOMAINS = [
    'http://test1.com.br',
    'http://test2.com.br',
    'http://test3.com'
]

host = 'Web Scenario'
group = 'Web'

#verificar se tem o host 'Web Scenario' 
ver_host = zapi.host.get(filter={'host': host} )

#verificar se tem o group 'Web' 
ver_group = zapi.hostgroup.get(filter={'name': group})

#Criar o host e o group caso não exista
if not ver_host:
    if not ver_group:
        zapi.hostgroup.create(name=group)

    groupid = zapi.hostgroup.get(filter={'name': group})
    zapi.host.create(host=host, groups=[{'groupid':groupid[0]['groupid']}], interfaces=[{'type':1, 'main':1,'useip':1,'ip':'192.168.10.138', 'dns':'', 'port': '10050'}])

# pegar as informações do host web scenario
hostid = zapi.host.get(filter={'host': host})

#pegar os dominios ja existentes no host
host_domains = zapi.httptest.get(filter={'hostid': hostid[0]['hostid']})


ver_domains = [url['name'] for url in host_domains]

# Se o dominio não existir ele cria

for i in DOMAINS:
    if i not in ver_domains:
        zapi.httptest.create(name= i,hostid= hostid[0]['hostid'], steps=[{'name': i, 'url': i, 'status_codes': '200','no':1}])
    zapi.trigger.create(description = '#URL# caiu'.replace('#URL#', i), expression= '{#HOST#:web.test.fail[#URL#].sum(#3)}=3'.replace('#URL#', i).replace('#HOST#', hostid[0]['host']),priority='5')



