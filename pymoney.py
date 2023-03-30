have = int(input('How much money do you have? '))
L = []
index = 0
while True:
    cmd = input('What do you want to do (add / view / delete / exit)? ')
    if cmd == 'add':
        print('Add an expense or income record with description and amount:')
        s = input()
        item = s.split(' ')
        amount = int(item[1])
        have += amount
        L.append(item)
        index += 1
        print(L)
    elif cmd == 'view':
        print("Here's your expense and income records:")
        print('{:20}{:6}'.format('Description', 'Amount'))
        print('='*20 + ' ' + '='*6)
        for i in range(index):
            print('{:2} {:18}{:6}'.format(i, L[i][0], L[i][1]))
        print('='*20 + ' ' + '='*6)
        print('Now you have {} dollars.'.format(have))
    elif cmd == 'delete':
        i = int(input('Which record do you want to delete? '))
        have -= int(L[i][1])
        index -= 1
        print('delete' + ' ' + L.pop(i)[0])
    elif cmd == 'exit':
        break
    else:
        pass