import sys

def initialize():
    """This open and read from a file that stores records.
    If cannot open or read the file, then prompt the user for initial money.
    """
    records = []
    try:
        fh = open('records.txt', 'r')
        initial_money = int(fh.readline())
        L = fh.readlines()
        for item in L:
            item = item[:-1].split(' ')
            d = dict(category=item[0], description=item[1], amount=int(item[2]))
            records.append(d)
    except:
        try:
            initial_money = int(input('How much money do you have? '))
        except ValueError:
            sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
            initial_money = 0
    else:
        print('Welcome back!')
        fh.close()
    return initial_money, records

def initialize_categories():
    """Initialize a categories list"""
    L = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    return L

def is_category_valid(category, categories):
    """Check if the category name is in the categories list"""
    if type(categories) == list:
        for v in categories:
            b = is_category_valid(category, v)
            if b == True:
                return True
    return categories == category
   
def add(initial_money, records, categories):
    """Add a record"""
    print('Add an expense or income record with category, description, and amount(separate by spaces):')
    item = input().split(' ')
    valid_category = is_category_valid(item[0], categories)
    if len(item) != 3 or not valid_category:
        if len(item) != 3:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
        elif not valid_category:
            sys.stderr.write('The specified category is not in the category list.\n')
            sys.stderr.write('You can check the category list by command "view categories".\n')
        sys.stderr.write('Fail to add a record.\n')
        return initial_money, records
    try:
        d = dict(category=item[0], description=item[1], amount=int(item[2]))
    except ValueError:
        sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
    else:
        initial_money += d['amount']
        records.append(d)
    return initial_money, records

def view(initial_money, records):
    """view the current records"""
    print("Here's your expense and income records:")
    print(f"   {'Category':<15} {'Description':<20} {'Amount':<6}")
    print(f"{'='*2} {'='*15} {'='*20} {'='*6}")
    for i, d in enumerate(records):
        print(f"{i:<2} {d['category']:15} {d['description']:20} {d['amount']:<6}")
    print(f"{'='*46}")
    print(f"Now you have {initial_money} dollars.")

def delete(initial_money, records):
    """delete a record from records"""
    try:
        i = int(input('Which line of record do you want to delete? '))
        initial_money -= records[i]['amount']
    except IndexError:
        sys.stderr.write(f'Index out of range. There if no line {i}.\n')
    except ValueError:
        sys.stderr.write('Invalid format. Fail to delete a record.\n')
    else:
        print(f'delete {records.pop(i)}')
    return initial_money, records

def view_categories(categories, level = -1):
    """view all the categories"""
    if type(categories) == list:
        for child in categories:
            view_categories(child, level+1)
    else:
        print(f'{" "*2*level}- {categories}')

def find_subcategories(category, categories):
    """Take a category name and return a non-nested list containing 
    the specified category and all the subcategories"""
    if type(categories) == list:
        for i, v in enumerate(categories):
            p = find_subcategories(category, v)
            if p == True:
                if (i + 1) < len(categories) and type(categories[i+1]) == list:
                    return flatten(categories[i:i+2])
                else:
                    return [v]
            if p != []:
                return p
    return  True if categories == category else []

def flatten(L):
    """Take a nested list and return a non-nested list"""
    if type(L) == list:
        result = []
        for child in L:
            result.extend(flatten(child))
        return result
    return [L]

def find(categories, records):
    """Prompt for a category name to find. Find all the records that belongs to that category.
    Print out the filtered records and report the total amount of money of the listed records."""
    category = input('Which category do you want to find? ')
    found_subcategories = find_subcategories(category, categories)
    if found_subcategories == []:
        sys.stderr.write('The specified category is not in the category list.\n')
        sys.stderr.write('You can check the category list by command "view categories".\n')
        return
    filtered_records = list(filter((lambda d: d['category'] in found_subcategories), records))
    print(f'Here\'s your expense and income records under category "{category}":')
    print(f"{'Category':<15} {'Description':<20} {'Amount':<6}")
    print(f"{'='*15} {'='*20} {'='*6}")
    total_amount = 0
    for d in filtered_records:
        print(f"{d['category']:15} {d['description']:20} {d['amount']:<6}")
        total_amount += d['amount']
    print(f"{'='*43}")
    print(f"The total amount above is {total_amount}.")

def save(initial_money, records):
    """Save the records to a file"""
    with open('records.txt', 'w') as fh:
        fh.write(f'{initial_money}\n')
        for item in records:
            fh.write(f"{item['category']} {item['description']} {item['amount']}\n")


initial_money, records = initialize()
categories = initialize_categories()

while True:
    cmd = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if cmd == 'add':
        initial_money, records = add(initial_money, records, categories)
    elif cmd == 'view':
        view(initial_money, records)
    elif cmd == 'delete':
        initial_money, records = delete(initial_money, records)
    elif cmd == 'view categories':
        view_categories(categories)
    elif cmd == 'find':
        find(categories, records)
    elif cmd == 'exit':
        save(initial_money, records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')