SECRET = 'xyzzy'

while True:
    password = input('Please enter your password: ')
    if not password:
        continue
    elif password == SECRET:
        break

    print('Wrong password!')


print('Welcome!')