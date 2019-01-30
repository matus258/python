#!/usr/bin/python3

for c in 'Hello World':
  print(c, end=' ')
  
for i in range(2, 20, 3):
  print(i)

print('\n')

for i, c in enumerate('Hello World!'):
  print(i, c)