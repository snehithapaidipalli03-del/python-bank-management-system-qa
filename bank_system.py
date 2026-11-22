
import json 
from customer_account import BankCustomer,SavingsAccount, AdvancedAccount
from admin import BankAdmin


# controls entire system,connects everything

accounts_list = []
admins_list = []

class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        
        #self.save_customers_to_file()   #
        
        self.load_customers_from_file()
        
        if not self.accounts_list:
            #self.load_bank_data() 
            self.load_default_customers()
            self.save_customers_to_file()
            
        self.load_admins()
    
    def load_bank_data(self):
        
        # create customers
        account_no = 1234
        customer_1 = BankCustomer("Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], account_no, 5000.00)
        self.accounts_list.append(customer_1)
        
        account_no+=1
        customer_2 = BankCustomer("David", "White", ["60", "Holborn Viaduct", "London", "EC1A 2FD"], account_no, 3200.00)    
        self.accounts_list.append(customer_2)

        account_no+=1
        customer_3 = BankCustomer("Alice", "Churchil", ["5", "Cardigan Street", "Birmingham", "B4 7BD"], account_no, 18000.00)
        self.accounts_list.append(customer_3)

        account_no+=1
        customer_4 = BankCustomer("Ali", "Abdallah",["44", "Churchill Way West", "Basingstoke", "RG21 6YR"], account_no, 40.00)
        self.accounts_list.append(customer_4)
                
        # create admins
    def load_admins(self):
        
        admin_1 = BankAdmin("id1188", "1441", True, "Julian", "Padget", ["12", "London Road", "Birmingham", "B95 7TT"])
        #self.admins_list.append(admin_1)

        admin_2 = BankAdmin("id3313", "2442", False, "Cathy",  "Newman", ["47", "Mars Street", "Newcastle", "NE12 6TZ"])
        #self.admins_list.append(admin_2)
        
        self.admins_list = [admin_1, admin_2]

   
   # 0r
    def generate_account_number(self):
       if not self.accounts_list:
           return 1000
       return max(c.get_account_no() for c in self.accounts_list) + 1 
   
    #created to get_account no.while creating customer account

    def search_admins_by_name(self, admin_username):
        #STEP A.2 - loop through the list -multiple admins listout
        found_admin = None
        for a in self.admins_list:
            if a.get_username() == admin_username:
                found_admin = a
                break
            
        if found_admin == None:   #if nothing found
            print("\n The Admin %s does not exist! Try again...\n" % admin_username)
        
        return found_admin
    
    #
        
    def search_customers_by_name(self, customer_lname):
        #STEP A.3 - admin doesnt know exact object - only name
        for customer in self.accounts_list:
            if customer.get_last_name().lower().strip() == customer_lname.lower().strip():
                return customer
            
        print("\n Customer" , customer_lname, "not found!")
        return None
      
     #
        
    def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option


    def run_main_options(self):
        loop = 1         
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input ("\n Please input admin username: ")
                password = input ("\n Please input admin password: ")
                msg, admin_obj = self.admin_login(username, password)
                print(msg)
                if admin_obj != None:
                    self.run_admin_options(admin_obj)
            elif choice == 2:
                loop = 0
        print ("\n Thank-You for stopping by the bank!")


    def transferMoney(self, sender_lname, receiver_lname, receiver_account_no, amount):
        #ToDo
        sender = None
        receiver = None
        
        #find  sender
        for c in self.accounts_list:
            if c.get_last_name().lower() == sender_lname.lower():
                sender = c
                break
        #find receiver (match Both name + account no)
        for c in self.accounts_list:
            if c.get_last_name() == receiver_lname and str(c.get_account_no()) == str(receiver_account_no):
                receiver = c
                break
        #validation
        if sender is None:
            print(" sender not found ")
            return 
        if receiver is None:
            print(" receiver not found ")
            return
        if sender.get_balance() < amount :
            print(" Insufficient balance ")
            return
        #transfer
        sender.withdraw(amount)
        receiver.deposit(amount)
        
        self.save_customers_to_file()
        
        print(" Transfer successful! ")
        return "Transfer Successful!"
    
    #
             
    def admin_login(self, username, password):
		  #STEP A.1
        found_admin = self.search_admins_by_name(username)
        msg = "\n Login failed"
        
        if found_admin != None:
            if found_admin.get_password() == password: #user exist->password
                msg = "\n Login successful"
            
        return msg, found_admin   #for user display , to allow further actions
    #
    
    def management_report(self):
        
        total_customers = len(self.accounts_list)
        
        total_balance  = 0
        total_overdraft = 0
        total_interest = 0
        
        for c in self.accounts_list:
            
            #total balance
            total_balance += c.get_balance()
            
            # overdraft (only for AdvancedAccount)
            if isinstance(c, AdvancedAccount):
                total_overdraft += c.get_overdraft_limit()
                
            #interest (only for savingsAccount)
            if isinstance(c, SavingsAccount):
                total_interest += c.get_balance() * c.get_interest_rate()
                 
        print("\n====== MANAGEMENT REPORT ======")
        print(" Total customers:", total_customers )
        print(" Total balance:", total_balance )
        print(" Total overdraft:", total_overdraft )
        print(" Total yearly interest:", total_interest )
        print(" =============================== ")

#############################


    def admin_menu(self, admin_obj):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s %s : Avilable options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Search Customer ")
         print ("3) Print all customers detail")
         print ("4) Update customer information ")
         print ("5) Delete customer ")
         print ("6) View admin details")
         print ("7) Update admin details")
         print ("8) Create new customer")
         print ("9) Management report")
         print ("10) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option

       
       
    def run_admin_options(self, admin_obj):                                
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin_obj)
            
     # Transfer Money
            if choice == 1:
                sender_lname = input("\n Please input sender surname: ")
                amount = float(input("\n Please input the amount to be transferred: "))
                if amount <=0:
                    print("Invalid amount")
                    continue
                receiver_lname = input("\n Please input receiver surname: ")
                receiver_account_no = int(input("\n Please input receiver account number: "))
                self.transferMoney(sender_lname, receiver_lname, receiver_account_no, amount)  
                
                
     
      ##search customer
            
            elif choice == 2:
                #Todo
                customer_name = input("\n Enter customer surname : ")
                customer = self.search_customers_by_name(customer_name)

                if customer != None:
                    customer.run_account_options()
                    
       ##customer details   
            elif choice == 3:
                #Todo
                for c in self.accounts_list:
                    c.print_details()
                    
       
                   
      
                    
     #  update info
            elif choice == 4:
                name = input("\n Enter customer surname: ")
                customer = self.search_customers_by_name(name)

                if customer != None:
                   fname = input(" Enter new first name: ")
                   lname = input(" Enter new last name: ")
                   customer.update_first_name(fname)
                   customer.update_last_name(lname)
    
                   house = input(" House no: ")
                   street = input(" Street: ")
                   city = input(" City: ")
                   postcode = input(" Postcode: ")
                   customer.update_address([house, street, city, postcode])
                   self.save_customers_to_file()
                   
                   print(" Customer updated successfully")

# delete customer
            elif choice == 5:
                #Todo
                customer_name = input("\n Enter customer surname to delete: ")
                customer = self.search_customers_by_name(customer_name)

                if customer != None:
                    self.accounts_list.remove(customer)
                    self.save_customers_to_file()
                    print(" Customer deleted successfully")
                    
    #View admin details
            elif choice == 6:
                admin_obj.print_details()
    
    #update admin details
            elif choice == 7:
                admin_obj.update_details()
                self.save_customers_to_file()
                
    #create new customer
            elif choice == 8:
                if admin_obj.has_full_admin_right():
                    fname = input("Enter first name: ")
                    lname = input("Enter last name: ")
                    
                    house = input("House no: ")
                    street = input("street: ")
                    city = input("City: ")
                    postcode = input("Postcode: ")
                    
                    balance = float(input("Enter initial balance: "))
                    
                    account_no = self.generate_account_number()
                    
                    print("\nSelect account type: ")
                    print("1) Savings Account ")
                    print("2) Advanced Account ")
                    
                    acc_type = int(input("Choose option: "))
                    
                    if acc_type == 1 :
                        interest = float(input("Enter interest rate (e.g.0.05): "))
                    
                        new_customer = SavingsAccount(
                            fname, lname,
                            [house, street, city, postcode],
                            account_no,
                            balance,
                            interest
                        )
                        
                    elif acc_type ==2:
                        overdraft = float(input("Enter overdraft limit: "))
                        
                        new_customer = AdvancedAccount(
                            fname, lname,
                            [house, street, city, postcode],
                            account_no,
                            balance,
                            overdraft
                        )
                    
                    else:
                        print("Invalid option")
                        return
                    
                    self.accounts_list.append(new_customer)
                    self.save_customers_to_file()
                    print("Customer created successfully ")
                    
                    
 #Management report feature
            elif choice == 9:
                self.management_report()
            
                
                


                
    #exit
            elif choice == 10:
                loop = 0
        print ("\n Exit account operations")
        
        
    ##save function
    def save_customers_to_file(self):
        data = []
        
        for c in self.accounts_list:
            customer_data ={
                "fname": c.get_first_name(),
                "lname": c.get_last_name(),
                "address": c.get_address(),
                "account_no": c.get_account_no(),
                "balance": c.get_balance()
             } 
        #saving
            if isinstance(c, SavingsAccount ):
                 customer_data["type"] = "savings"
                 customer_data["interest"] = c.get_interest_rate()
            
            elif isinstance(c, AdvancedAccount ):
                customer_data["type"] = "advanced"
                customer_data["overdraft"] = c.get_overdraft_limit()
                
            else:
                customer_data["type"] = "basic"  
                 
            data.append(customer_data)
            
        with open("customers.json", "w") as file:
            json.dump(data, file, indent=4)
        
        print(" Customers saved to file")
        
        
    ##Load function
    def load_customers_from_file(self):
        try:
            with open("customers.json","r") as file:
                data = json.load(file)
            
            self.accounts_list = []
                
            for c in data:
                
                acc_type = c.get("type")
                
                if acc_type == "savings":
                    customer = SavingsAccount(
                        c["fname"], c["lname"], c["address"], c["account_no"], c["balance"], c.get("interest", 0.05) #0.05 #default interest
                    )
                    
                elif acc_type == "advanced":
                    customer = AdvancedAccount(
                        c["fname"], c["lname"], c["address"], c["account_no"], c["balance"], c.get("overdraft", 500) #500  #default overdraft
                    )
                    
                else: 
                    customer = BankCustomer(
                        c["fname"], c["lname"], c["address"], c["account_no"], c["balance"]
                 
                    )
                    
                self.accounts_list.append(customer)
                    
            print("Customers loaded from file")   # outside loop
            
        except FileNotFoundError:
            print(" No file found, starting fresh ")
            
if __name__ == "__main__":         
    app = BankSystem()
    app.run_main_options()

##------------------->>>>>>>>>>>>>>>>>>>>

