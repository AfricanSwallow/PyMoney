import sys

def initialize():
    records = []
    try:
        fh = open('records.txt', 'r')
        initial_money = int(fh.readline())
        L = fh.readlines()
        for item in L:
            item = item[:-1]
            records.append(item.split(' '))
    except:
        try:
            initial_money = int(input('How much money do you have? '))
        except ValueError:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            initial_money = 0
    else:
        print('Welcome back!')
        fh.close()
    return (initial_money, records)
    
def add(initial_money, records):
    print('Add an expense or income record with description and amount:')
    s = input()
    item = s.split(' ')
    if len(item) != 2:
        sys.stderr.write('The format of a record should be like this: breakfast -50.\n')
        sys.stderr.write('Fail to add a record.\n')
        return records
    
    try:
        amount = int(item[1])
    except ValueError:
        sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
    else:
        initial_money += amount
        records.append(item)
    return (initial_money, records)

def view(initial_money, records):
    print("Here's your expense and income records:")
    print('   {:^17}{:6}'.format('Description', 'Amount'))
    print('='*2 + ' ' + '='*16 + ' ' + '='*6)
    for i in range(len(records)):
        print('{:<2} {:<17}{:<6}'.format(i, records[i][0], records[i][1]))
    print('='*2 + ' ' + '='*16 + ' ' + '='*6)
    print('Now you have {} dollars.'.format(initial_money))

def delete(initial_money, records):
    i = int(input('Which line of record do you want to delete? '))
    try:
        initial_money -= int(records[i][1])
    except IndexError:
        sys.stderr.write(f'Index out of range. There if no line {i}.\n')
    except ValueError:
        sys.stderr.write('Invalid format. Fail to delete a record.\n')
    else:
        print(f'delete {records.pop(i)[0]}')
    return initial_money, records

def save(initial_money, records):
    with open('records.txt', 'w') as fh:
        fh.write(f'{initial_money}\n')
        for item in records:
            fh.write(f'{item[0]} {item[1]}\n')


initial_money, records = initialize()

while True:
    cmd = input('\nWhat do you want to do (add / view / delete / exit)? ')
    if cmd == 'add':
        initial_money, records = add(initial_money, records)
    elif cmd == 'view':
        view(initial_money, records)
    elif cmd == 'delete':
        initial_money, records = delete(initial_money, records)
    elif cmd == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')