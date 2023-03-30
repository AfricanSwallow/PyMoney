import sys
L = []
index = 0


try:
    fh = open('records.txt', 'r')
    have = int(fh.readline())
    records = fh.readlines()
    print(have)
    print(records)
    for item in records:
        item = item[:-1]
        print(f'index:{index} {item}')
        L.append(item.split(' '))
        index += 1
except:
    try:
        have = int(input('How much money do you have? '))
    except ValueError:
        sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
        have = 0
else:
    fh.close()


while True:
    cmd = input('\nWhat do you want to do (add / view / delete / exit)? ')
    if cmd == 'add':
        print('Add an expense or income record with description and amount:')
        s = input()
        item = s.split(' ')
        if len(item) != 2:
            sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
            sys.stderr.write('Fail to add a record.\n')
            continue
        
        try:
            amount = int(item[1])
        except ValueError:
            sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
        else:
            have += amount
            L.append(item)
            index += 1
            # print(L)

    elif cmd == 'view':
        print("Here's your expense and income records:")
        print('   {:^17}{:6}'.format('Description', 'Amount'))
        print('='*2 + ' ' + '='*16 + ' ' + '='*6)
        for i in range(index):
            print('{:2} {:18}{:6}'.format(i, L[i][0], L[i][1]))
        print('='*2 + ' ' + '='*16 + ' ' + '='*6)
        print('Now you have {} dollars.'.format(have))

    elif cmd == 'delete':
        i = int(input('Which line of record do you want to delete? '))
        try:
            have -= int(L[i][1])
        except IndexError:
            sys.stderr.write(f'Index out of range. There if no line {i}.\n')
        except ValueError:
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
        else:
            index -= 1
            # print('delete' + ' ' + L.pop(i)[0] + '\n')
            print(f'delete {L.pop(i)[0]}')

    elif cmd == 'exit':
        break

    else:
        sys.stderr.write('Invalid command. Try again.\n')

with open('records.txt', 'w') as fh:
    fh.write(f'{have}\n')
    for item in L:
        fh.write(f'{item[0]} {item[1]}\n')
    