#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests


import json
import sys

#IPconsultado passado por parametro/argumento no script
ip_RBL = sys.argv

#Concatenação de endereço da api + IP consultado
url = ("https://api.xforce.ibmcloud.com/ipr/%s" %(ip_RBL[1]))

#Obtem dados do IP consultado
apiibm = requests.get(url,auth=('531cf2df-5ede-42fd-a380-c271ebf19c7d','6d49758a-c91c-4c59-9c64-a8b079a55e3b'))

#converte conteudo em Json
apiibmjson=json.loads(apiibm.content)

#Retorna o score do IP
print(apiibmjson['score'])
