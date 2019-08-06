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
    resp = []
    printa = []
    tamProAux= tamPro.copy()
    for t in tamPar:
        i = 0
        try:
            while True:
                if int(tamProAux[i])<= int(t):
                    resp.append((t+'   '+tamProAux[i]))
                    tamProAux.remove(tamProAux[i])
                    printa.append(tamPar.index(t))
                    break
                else:
                    i +=1
        except IndexError:
            pass
    for test in range(int(n)):
        try:
            print(resp[printa.index(test)])
        except ValueError:
            print(tamPar[test]+'  vazio')
def worst(numPar,tamPar, numPro, tamPro):
    print('Worst')
    print('SO  SO')
    l = []
    printa= []
    tamAux =tamPar.copy()
    resp = []
    for t in tamPro:
        c = 0
        s = []
        for p in tamAux:
            if int(t)<= int(p):
                s.append(int(p)-int(t))
        sobra= max(s, key=int, default=0)
        for i in tamAux:
            if int(i)-int(t) == sobra:
                resp.append(i+'   '+t)
                tamAux.remove(i)
                printa.append(tamPar.index(i))
            c += 1
    for test in range(int(n)):
        try:
            print(resp[printa.index(test)])
        except ValueError:
            print(tamPar[test]+'  vazio')

def best(numPar,tamPar, numPro, tamPro):
    print('Best')
    print('SO  SO')
    l = []
    printa= []
    tamAux =tamPar.copy()
    resp = []
    for t in tamPro:
        c = 0
        s = []
        for p in tamAux:
            if int(t)<= int(p):
                s.append(int(p)-int(t))
        sobra = min(s, key=int,default=0)
        for i in tamAux:
            if int(i)-int(t) == sobra:
                resp.append(i+'   '+t)
                tamAux.remove(i)
                printa.append(tamPar.index(i))
            c += 1
    for test in range(int(n)):
        try:
            print(resp[printa.index(test)])
        except ValueError:
            print(tamPar[test]+'  vazio')
first(n,tamPar,p,tamPro)
worst(n,tamPar,p,tamPro)
best(n,tamPar,p,tamPro)