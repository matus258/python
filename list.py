#!/usr/bin/python3

# lista vazia
l = list()

# acrescentando valores
l.extend(['apple', 'uva', 'melon', 'banana'] )

print(l,'\n')

#inserindo valor em posição especifica
l.insert(3, 'abacaxi')

print(l,'\n')

#deletando um valor
# del l[3]

print(l,'\n')

#Exclui o valor do ultimo indice
# print(l.pop(),'\n')

#Exclui o valor de um indice especifico
# print(l.pop(2),'\n')

#troca um elemento por um referenciado
l[0] =  'oi'

print(l,'\n')

#tamanho da lista
print(len(l))

#Retorna o ultimo valor da lista
print(l[-1])

#Retorna o indice 2 e o 4
print(l[2:4])

