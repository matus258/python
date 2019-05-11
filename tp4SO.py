#!/usr/bin/python3
n = input('Digite o numero de particoes: ')
tamPar = []
for t in range(int(n)):
    tamPar.append(input('Digite o tamanho da particao '+str(t+1)+': '))
p = input('Digite o numero de processos: ')
tamPro = []
for t in range(int(p)):
    tamPro.append(input('Digite o tamanho do processo:'+str(t+1)+': '))

def first(numPar,tamPar, numPro, tamPro):
    print('First')
    print('SO  SO')
    for t in tamPar:
        i = 0
        while True:
            if int(tamPro[i])<= int(t):
                print(t+'   '+tamPro[i])
                break
            else:
                i +=1
def worst(numPar,tamPar, numPro, tamPro):
    print('Worst')
    print('SO  SO')
    l = []
    printa= []
    tamAux = tamPar
    resp = []
    for t in tamPro:
        c = 0
        s = []
        for p in tamAux:
            if int(t)<= int(p):
                s.append(int(p)-int(t))
        sobra = 0
        for d in s:
            if sobra < d:
                sobra = d
        for i in tamAux:
            if int(i)-int(t) == sobra:
                resp.append(i+'   '+t)
                tamAux.remove(i)
                printa.append(c)
            c += 1
    for test in range(len(resp)):

        print(resp[printa.index(test)])

worst(n,tamPar,p,tamPro)