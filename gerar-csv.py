#!/usr/bin/python3

import csv
import os

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
    spamwriter.writerow(['Marca', 'modelo'])

print('Arquivo gerado no diretorio: ' + arquivoOutput)