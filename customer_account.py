class BankCustomer:
    def __init__(self, fname, lname, address, account_no, balance):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)
    
    def update_first_name(self, fname):
        self.fname = fname
    
    def update_last_name(self, lname):
        self.lname = lname
                
    def get_first_name(self):
        return self.fname
    
    def get_last_name(self):
        return self.lname
        
    def update_address(self, addr):
        self.address = addr
        
    def get_address(self):
        return self.address
    
    def deposit(self, amount):   # add money
        self.balance+=amount

   #     
    def withdraw(self, amount):  # prevent negative balance, invalid transactions
        #ToDo
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False
     #
     
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
        
    def get_balance(self):
        return self.balance         # current object(separate different balance )
    
    def get_account_no(self):
        return self.account_no
    
    def get_account_type(self):
        if isinstance(self, SavingsAccount):
            return "Savings Account"
        elif isinstance(self, AdvancedAccount):
            return "Advanced Account"
        else:
            return "Basic Account"
    
    def account_menu(self):
        print ("\n Your Transaction Options Are:")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Deposit money")
        print ("2) Withdraw money")
        print ("3) Check balance")
        print ("4) Update customer name")
        print ("5) Update customer address")
        print ("6) Show customer details")
        print ("7) Back")
        #print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    def print_details(self):         # clean , reusable, OOPs concept
        #STEP A.4.3
        print("First name:", self.fname)
        print("Last name:", self.lname)
        print("Account No:", self.account_no)
        print("Address:", self.address[0])
        print(" ", self.address[1])
        print(" ", self.address[2])
        print(" ", self.address[3])
        if isinstance(self, SavingsAccount):     #############
            acc_type = "Savings Account"
        elif isinstance(self, AdvancedAccount):
            acc_type = "Advanced Account"
        else:
            acc_type = "Basic Account"

        print("Account Type:", acc_type)
        print("Balance:%.2f" % self.balance)
        print(" ")
    #
        
    def run_account_options(self):        #While loop- perform multipla actions
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                #STEP A.4.1
               amount = float(input("\n Enter amount to deposit: "))
               if amount <=0:
                   print("Invalid amount")
                   continue
               
               old_balance = self.balance
               self.deposit(amount)
               
               print("\n Deposit Successful")
               print(f"Previous Balance: £{old_balance:.2f}")
               print(f"Deposited Amount: £{amount:.2f}")
               print(f"New Balance: £{self.balance:.2f}")
               
    #
            elif choice == 2:
                #ToDo
                amount = float(input("\n Enter amount to withdraw: "))
                if amount<=0:
                    print("Invalid amount")
                    continue
                
                old_balance = self.balance
                success = self.withdraw(amount)
    
                if success:
                    print("\n Withdraw Successful")
                    print(f"Previous Balance: £{old_balance:.2f}")
                    print(f"Withdrawn Amount: £{amount:.2f}")
                    print(f"New Balance: £{self.balance:.2f}")
                else:
                    print("Insufficient funds (or overdraft limit reached)")
                
    #
            elif choice == 3:
                #STEP A.4.4
                self.print_balance()
    #
            elif choice == 4:
                #STEP A.4.2
                fname = input("\n Enter new first name: ")
                self.update_first_name(fname)
                
                lname = input("\n Enter new last name: ")
                self.update_last_name(lname)
    #
                
            elif choice == 5:
                #ToDo
                house = input("House no: ")
                street = input("street: ")
                city = input("City: ")
                postcode =input("Postcode: ")
                
                self.update_address([house, street, city, postcode])
    #
                
            elif choice == 6:
                self.print_details()
            elif choice == 7:
                loop = 0
        print ("\n Exit account operations")
        
    #adding savings account class
    
class SavingsAccount(BankCustomer):
    
    def __init__(self, fname, lname, address, account_no, balance, interest_rate):
        super().__init__(fname, lname, address, account_no, balance)
        self.interest_rate = interest_rate
       
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        
    def get_interest_rate(self):
        return self.interest_rate
        
    #adding advanced account class
 
class AdvancedAccount(BankCustomer):
    def __init__(self, fname, lname, address, account_no, balance, overdraft_limit):
        super().__init__(fname, lname, address, account_no, balance)
        self.overdraft_limit = overdraft_limit
        
    def withdraw(self, amount):
        if self.balance - amount >= -self.overdraft_limit:
            self.balance -= amount
            return True
        else:
            return False
        
    def get_overdraft_limit(self):
        return self.overdraft_limit
        