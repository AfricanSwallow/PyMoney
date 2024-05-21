import sys
# hi
# plan B

class Record:
    """Represent a record."""
    def __init__(self, category, description, amount):
        self._category = category
        self._descripttion = description
        self._amount = amount

    @property
    def category(self):
        return self._category
    @property
    def description(self):
        return self._descripttion
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        self._records = []
        try:
            fh = open('records.txt', 'r')
            self._initial_money = int(fh.readline())
            L = fh.readlines()
            for item in L:
                item = item[:-1].split(' ')
                r = Record(category=item[0], description=item[1], amount=int(item[2]))
                self._records.append(r)
        except:
            try:
                self._initial_money = int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                self._initial_money = 0
        else:
            print('Welcome back!')
            fh.close()

    def add(self, record, categories):
        """Add a record"""
        record = record.split()
        valid_category = categories.is_category_valid(record[0])
        if len(record) != 3 or not valid_category:
            if len(record) != 3:
                sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n')
            elif not valid_category:
                sys.stderr.write('The specified category is not in the category list.\n')
                sys.stderr.write('You can check the category list by command "view categories".\n')
            sys.stderr.write('Fail to add a record.\n')
            return
        try:
            r = Record(category=record[0], description=record[1], amount=int(record[2]))
        except ValueError:
            sys.stderr.write('Invalid value for money.\nFail to add a record.\n')
        else:
            self._initial_money += r.amount
            self._records.append(r)

    def view(self):
        """view the current records"""
        print("Here's your expense and income records:")
        print(f"   {'Category':<15} {'Description':<20} {'Amount':<6}")
        print(f"{'='*2} {'='*15} {'='*20} {'='*6}")
        for i, r in enumerate(self._records):
            print(f"{i:<2} {r.category:15} {r.description:20} {r.amount:<6}")
        print(f"{'='*46}")
        print(f"Now you have {self._initial_money} dollars.")

    def delete(self, delete_record):
        """delete a record from records"""
        try:
            i = int(delete_record)
            self._initial_money -= self._records[i].amount
        except IndexError:
            sys.stderr.write(f'Index out of range. There if no line {i}.\n')
        except ValueError:
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
        else:
            print(f'delete {self._records.pop(i)}')

    def find(self, target_categories, category):
        """Prompt for a category name to find. Find all the records that belongs to that category.
        Print out the filtered records and report the total amount of money of the listed records."""
        if target_categories == []:
            sys.stderr.write('The specified category is not in the category list.\n')
            sys.stderr.write('You can check the category list by command "view categories".\n')
            return
        filtered_records = list(filter((lambda r: r.category in target_categories), self._records))
        print(f'Here\'s your expense and income records under category "{category}":')
        print(f"{'Category':<15} {'Description':<20} {'Amount':<6}")
        print(f"{'='*15} {'='*20} {'='*6}")
        total_amount = 0
        for r in filtered_records:
            print(f"{r.category:15} {r.description:20} {r.amount:<6}")
            total_amount += r.amount
        print(f"{'='*43}")
        print(f"The total amount above is {total_amount}.")

    def save(self):
        """Save the records to a file"""
        with open('records.txt', 'w') as fh:
            fh.write(f'{self._initial_money}\n')
            for r in self._records:
                fh.write(f"{r.category} {r.description} {r.amount}\n")

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view(self):
        """view all the categories"""
        def view_categories(categories = self._categories, level = -1):
            if type(categories) == list:
                for child in categories:
                    view_categories(child, level+1)
            else:
                print(f'{" "*2*level}- {categories}')
        view_categories()
        
    
    def is_category_valid(self, category):
        """Check if the category name is in the categories list"""
        def is_valid(category, categories):
            if type(categories) == list:
                for v in categories:
                    b = is_valid(category, v)
                    if b == True:
                        return True
            return categories == category
        return is_valid(category, self._categories)

    def find_subcategories(self, category):
        """Take a category name and return a non-nested list containing 
            the specified category and all the subcategories"""
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                    and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found:
                    yield categories
        return [i for i in find_subcategories_gen(category, self._categories)]


categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add an expense or income record with category, description, and amount(separate by spaces):\n')
        records.add(record, categories)        
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input('Which line of record do you want to delete? ')
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories, category)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
        
print("hello world")