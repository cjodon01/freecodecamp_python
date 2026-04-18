"""
Author: Cory Jodon
Description: Completed budget app for free code camp.org exercise. 
"""
class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = []
    
    def __str__(self):
        # 1. Create the title line (Centered, 30 chars wide, padded with '*')
        title = f"{self.name:*^30}\n"
        
        # 2. Build the ledger entries string
        items = ""
        for item in self.ledger:
            # Truncate description to 23 chars and left-align
            desc = f"{item['description'][:23]:<23}"
            
            # Format amount to 2 decimal places and right-align to 7 chars
            amt = f"{item['amount']:>7.2f}"
            
            # Append the formatted line to the items string
            items += f"{desc}{amt}\n"
            
        # 3. Create the final Total line
        total = f"Total: {self.get_balance()}"
        
        # 4. Combine and return
        return title + items + total


    def deposit(self,amount,description=""):
        self.ledger.append({'amount': amount, 'description': description})
        self.get_balance()

    def withdraw(self,amount,description=""):
        self.ledger.append({'amount': (amount*-1), 'description': description})
        balance = self.get_balance()
        if amount > balance:
            print(f"Insufficient Funds. Balance:${balance}")
            return False
        return True
    
    def get_balance(self):
        balance = 0
        #print(self.ledger)
        for index,item in enumerate(self.ledger):
            balance += item['amount']
        return balance
    
    def transfer(self,amount,catagory):
        if not self.check_funds(amount):
            return False
        self.ledger.append({'amount': -1*amount, 'description': f"Transfer to {catagory.name}"})
        catagory.deposit(amount, f"Transfer from {self.name}")
        return True
        

    def check_funds(self,amount):
        if amount > self.get_balance():
            return False
        return True
def create_spend_chart(categories):
   total_spend = 0
   cat_table = []
   for cat in categories:
        cat_spend = 0
        if cat.ledger:
            for item in cat.ledger:
                if item['amount'] < 0:
                    cat_spend += item['amount'] *-1
                    total_spend += item['amount']*-1
            cat_table.append({"category": cat.name,"amount": cat_spend,"percent":0})
            for item in cat_table:
                item['percent'] = (item['amount']/total_spend  *100) // 10 * 10
        else:
            cat_table.append({"category": cat.name,"amount": 0,"percent":0})
        chart = "Percentage spent by category\n"
   for value in range (100,-1,-10):
        chart += f"{value:>3}| "
        for item in cat_table:
            if item['percent'] >= value:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"
   chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

   names = [category['category'] for category in cat_table]

   max_len = max([len(name) for name in names])
   for i in range(max_len):
        chart += "     "  # 5 spaces for left margin under the bars
        for name in names:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   "
        if i != max_len - 1:
            chart += "\n"

   return chart


food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
gas = Category("Gas")
gas.deposit(2000,'initial deposit')
gas.withdraw(128,'fill up')
food.transfer(50, clothing)
#print(food)

print(create_spend_chart([food,clothing,gas]))


"""

class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = []
    
    def __str__(self):
        # 1. Create the title line (Centered, 30 chars wide, padded with '*')
        title = f"{self.name:*^30}\n"
        
        # 2. Build the ledger entries string
        items = ""
        for item in self.ledger:
            # Truncate description to 23 chars and left-align
            desc = f"{item['description'][:23]:<23}"
            
            # Format amount to 2 decimal places and right-align to 7 chars
            amt = f"{item['amount']:>7.2f}"
            
            # Append the formatted line to the items string
            items += f"{desc}{amt}\n"
            
        # 3. Create the final Total line
        total = f"Total: {self.get_balance()}"
        
        # 4. Combine and return
        return title + items + total


    def deposit(self,amount,description=""):
        self.ledger.append({'amount': amount, 'description': description})
        self.get_balance()

    def withdraw(self,amount,description=""):
        self.ledger.append({'amount': (amount*-1), 'description': description})
        balance = self.get_balance()
        if amount > balance:
            print(f"Insufficient Funds. Balance:${balance}")
            return False
        return True
    
    def get_balance(self):
        balance = 0
        #print(self.ledger)
        for index,item in enumerate(self.ledger):
            balance += item['amount']
        return balance
    
    def transfer(self,amount,catagory):
        if not self.check_funds(amount):
            return False
        self.ledger.append({'amount': -1*amount, 'description': f"Transfer to {catagory.name}"})
        catagory.deposit(amount, f"Transfer from {self.name}")
        return True
        

    def check_funds(self,amount):
        if amount > self.get_balance():
            return False
        return True
def create_spend_chart(categories):
    # 1. Calculate total SPENT per category (withdrawals only)
    spent_amounts = []
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:  # Only count withdrawals (negative amounts)
                spent += abs(item["amount"])
        spent_amounts.append(spent)
        
    total_spent = sum(spent_amounts)

    # 2. Calculate percentages rounded DOWN to the nearest 10
    percentages = []
    for amount in spent_amounts:
        # Multiply by 100, floor divide by 10, then multiply by 10
        percent = int((amount / total_spent) * 100) // 10 * 10
        percentages.append(percent)

    # 3. Build the chart string
    chart = "Percentage spent by category\n"
    
    # --- Y-Axis and Bars ---
    for value in range(100, -1, -10):
        chart += f"{value:>3}| "
        for percent in percentages:
            if percent >= value:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    # --- Horizontal Dashed Line ---
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # --- X-Axis (Vertical Category Names) ---
    # Extract just the names into a list
    names = [category.name for category in categories]
    max_len = max([len(name) for name in names])
    
    for i in range(max_len):
        chart += "     "  # 5 spaces for left margin under the bars
        for name in names:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   "
        
        # Add a newline for every row EXCEPT the very last one
        if i != max_len - 1:
            chart += "\n"

    # Return the complete string instead of just the title
    return chart


food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
#print(food)

print(create_spend_chart([food,clothing]))

"""
