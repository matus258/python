#!/usr/bin/python3

l = list()

l.extend(['cebola','amora','jaca', 'banana', 'pera'])

tamanho = len(l)

for i in range(tamanho):
    for j in range(tamanho):
        if l[i] < l[j]:
            aux = l[i]
            l[i] = l[j]
            l[j] = aux
print(l)