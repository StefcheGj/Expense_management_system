import db_connector
import read_expenses
import numpy
import currency_converter

DATABASE_NAME = "cost_management.db"
mysql_db1 = db_connector.connectDB(DATABASE_NAME)

def statistics_menu():
    print("Welcome to the statistic menu. What statistics would you like to see?\n1. Cheapest/most expensive item\n2. Total average/median spent\n3. spent in 1 month / 3 months / 1 year")
    user_input = input("Please enter a number: ")
    while not user_input.isdigit():
        print("Please, enter a digit.")
    user_input = int(user_input)
    if user_input not in (1,2,3):
        print("Ur input was invalid. Please make a choice over again in the menu.")
        statistics_menu()
    elif user_input == 1:
        get_cheapest_most_expensive_item()
    elif user_input == 2:
        print("What kind of the following information would you like to see?\n1. The average of my expenses\n2. The median of my expenses")
        user_input = input("Please enter a number for your choice (1 or 2): ")
        while not user_input.isdigit():
            print("please enter a digit")
        if user_input == "1":
            print("here we are in opt 1")
            average_of_expenses()
        elif user_input == "2":
            median_of_expenses()
        else:
            print("Your choice is invalid. You will be send back to the statistic menu.")
            statistics_menu()
    elif user_input == 3:
        print("What would you like to see?\n1. My expenses for a certain month\n2. My expenses for 3 months\n3. My expenses for a certain year")
        user_input = input("Enter a number please: ")
        while not user_input.isdigit():
            print("Please enter a valid digit (1, 2 or 3).")
        if user_input == "1":
            expenses_for_1_month()
        elif user_input == "2":
            expenses_for_3_months()
        elif user_input == "3":
            expenses_for_a_year()
        


def get_cheapest_most_expensive_item():
    print("")
    print("Are you searching for the cheapest or most expensive item? (please enter a number)\n1. Cheapest\n2. Most expensive")
    try:
        user_input = int(input(""))
    except:
        user_input = 0
    if user_input == 1:
        print("")
        item, cost = cheapest_item()
        print(f"The cheapest item is: {item}, which costs {cost}.")
    if user_input == 2:
        print("")
        item, cost = most_expensive_item()
        print(f"The most expensive item is: {item}, which costs {cost}.")


def decorator_of_currency(func1):
    def wrapper():
        item, cost = func1()
        certain_currency = "INR"                            # take it from the settings_table
        new_cost = cost * currency_converter.get_exchange_rate(certain_currency)
        print("The currency is being translated to:", certain_currency)
        return item, new_cost
    return wrapper

@decorator_of_currency
def most_expensive_item():
    dict1 = {tpl[0] : tpl[1] for tpl in read_expenses.check_all_expenses(print_results=False)}
    highest_value = 0
    the_item = ""
    for k,v in dict1.items():
        if v > highest_value:
            highest_value = v
            the_item = k
    return the_item, highest_value



@decorator_of_currency
def cheapest_item():
    dict2 = {tpl[0] : tpl[1] for tpl in read_expenses.check_all_expenses(print_results= False)}
    lowest_number = 700
    the_item = ""
    for k,v in dict2.items():
        if v < lowest_number:
            lowest_number = v
            the_item = k
    print(f"item: {the_item}, cost:  {lowest_number},-")
    return the_item , lowest_number



def get_total_expenses():
    list_of_expenses = [pr[1] for pr in read_expenses.check_all_expenses(print_results=False)]
    total_expenses = 0
    for i in list_of_expenses:
        total_expenses = total_expenses + i
    return total_expenses

def average_of_expenses(print_result = True):
    the_final_average = get_total_expenses() / len(read_expenses.check_all_expenses(print_results=False))
    if print_result == True:
        print(f"The final average of your costs is {round(the_final_average, 1)}.")
    return round(the_final_average, 1)

def median_of_expenses(print_results = True):
    list_of_expenses = [pr[1] for pr in read_expenses.check_all_expenses(print_results=False)]
    the_median = numpy.median(list_of_expenses)
    if print_results == True:
        print(f"The median of your expenses is: {the_median}.")
    return the_median



def expenses_for_1_month():
    print("\nWelcome to the expense tracer!")
    any_year = input("Enter the year you wanna filter on (yyyy): ")
    any_month = input("Enter the month you wanna filter on (mm): ")
    exact_date = any_year + "-" + any_month
    month_expenses = 0
    dict1 = {clmn[1] : clmn[2] for clmn in read_expenses.check_all_expenses(print_results=False)}
    for cost,date_time in dict1.items():
        if date_time.startswith(exact_date):
            month_expenses = month_expenses + cost
    print(f"your expenses for {exact_date} are in total: € {month_expenses},-")
    return month_expenses




def expenses_for_3_months():
    year_dict = {1: 2023, 2 : 2024, 3 : 2025}
    print("In what year are the expenses you want to check?\n1. 2023\n2. 2024\n3. 2025")
    user_input1 = int(input("Enter a number please (1, 2 or 3): "))
    selected_year = str(year_dict[user_input1])
    month_dict = {1 : ("01", "02", "03"), 2 : ("04", "05", "06"), 3 : ("07", "08", "09"), 4 : ("10", "11", "12")}
    print("\nWhich trimester would you like to track?\n1. january - february - march\n2. april - may - june\n3. july - august - september\n4. october - november - december")
    user_input2 = int(input("Enter the number of the trimester please (1, 2, 3 or 4): "))
    selected_month = str(month_dict[user_input2])
    dict1 = {x[1] : x[2] for x in read_expenses.check_all_expenses(print_results=False)}
    filtered_expenses = {prijs : datum for prijs, datum in dict1.items() if datum.startswith(selected_year) and datum[5:7] in selected_month}
    expenses_for_trimester = 0
    if filtered_expenses:
        print(f"Your expenses for trimester {selected_month} in year {selected_year}")
        for prijs, datum in filtered_expenses.items():
            expenses_for_trimester = expenses_for_trimester + prijs
        print(f"The total amount of expenses that period was: {expenses_for_trimester} euro's.")
        return expenses_for_trimester


def expenses_for_a_year():
    dict5 = {x[1] : x[2] for x in read_expenses.check_all_expenses(print_results=False)}
    expense_year = {1 : 2023, 2 : 2024, 3 : 2025}
    user_input = int(input("For which year would you like to see your expenses?\n1. 2023\n2. 2024\n3. 2025\nPlease enter a number: "))
    choice_of_year = str(expense_year[user_input])
    sum_of_costs = 0
    for prijs,datum in dict5.items():
        if datum.startswith(choice_of_year):
            sum_of_costs = sum_of_costs + prijs
    print(sum_of_costs)
    return sum_of_costs









statistics_menu()
    





# statistics of: cheapest/most expensive item, item-cost average, how much spent per month, how much spent in 3 months, how much spent per year
# median spent
# how much % spent for school/work, how much for groceries, how much for household goods etc. #v2
# Consider missing values within the table.
