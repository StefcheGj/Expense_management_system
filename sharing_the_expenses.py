import db_connector


DATABASE_NAME = "cost_management.db"
mysql_db1 = db_connector.connectDB(DATABASE_NAME)


def sharing_the_expenses():
    print("This is the new line of code")
    print("Via what media would you like to share your expenses?\n1. WhatsApp \n2. LinkedIn \n3. Gmail")
    try:
        user_input = int(input("Please enter a number to indicate: "))
    except:
        user_input = 0
    if user_input == 1:
        print("Sharing on WhatsApp...")
    elif user_input == 2:
        print("Sharing on LinkedIn...")
    elif user_input == 3:
        print("Sharing on Gmail")
    else:
        sharing_the_expenses()
