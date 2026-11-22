# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:33:31 2026

@author: Snehitha

"""


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>....
import tkinter as tk
from tkinter import ttk, messagebox
from bank_system import BankSystem
from customer_account import SavingsAccount, AdvancedAccount


class BankGUI:
    def __init__(self):
        self.system = BankSystem()
        self.admin = None

        self.root = tk.Tk()
        self.root.title("Bank Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="white")

        self.login_screen()
        self.root.mainloop()

    # ---------------- CLEAR RIGHT PANEL ----------------
    def clear_right(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    # ---------------- LOGIN ----------------
    def login_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="BANK MANAGEMENT SYSTEM",
                 font=("Arial", 26, "bold"), bg="white").pack(pady=40)

        frame = tk.Frame(self.root, bg="white")
        frame.pack()

        tk.Label(frame, text="Username", bg="white").grid(row=0, column=0, pady=10)
        self.username = tk.Entry(frame)
        self.username.grid(row=0, column=1)

        tk.Label(frame, text="Password", bg="white").grid(row=1, column=0, pady=10)
        self.password = tk.Entry(frame, show="*")
        self.password.grid(row=1, column=1)

        tk.Button(frame, text="Login", width=20,
                  command=self.check_login).grid(row=2, columnspan=2, pady=20)

    def check_login(self):
        msg, admin = self.system.admin_login(self.username.get(), self.password.get())
        if admin:
            self.admin = admin
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Login")

    # ---------------- DASHBOARD ----------------
    def dashboard(self):
        for w in self.root.winfo_children():
            w.destroy()

        # LEFT MENU
        self.left_frame = tk.Frame(self.root, bg="#1f2a44", width=250)
        self.left_frame.pack(side="left", fill="y")

        # RIGHT PANEL
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="right", expand=True, fill="both")

        tk.Label(self.left_frame, text=f"Admin\n{self.admin.get_first_name()}",
                 bg="#1f2a44", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

        buttons = [
            ("View Customer", self.view_customer),
            ("Print All Customers", self.print_all),
            ("Update Customer", self.update_customer),
            ("Delete Customer", self.delete_customer),
            ("View Admin", self.view_admin),
            ("Update Admin", self.update_admin),
            ("Create Customer", self.create_customer),
            ("Management Report", self.report),
            ("Logout", self.login_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.left_frame, text=text, width=25,
                      bg="#34495e", fg="white",
                      command=cmd).pack(pady=5)

    # ---------------- VIEW SINGLE CUSTOMER ----------------
    def view_customer(self):
        self.clear_right()

        tk.Label(self.right_frame, text="View Customer",
                 font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        entry = tk.Entry(self.right_frame)
        entry.pack()

        def show():
            c = self.system.search_customers_by_name(entry.get())
            if c:
                self.clear_right()

                tk.Label(self.right_frame, text="Customer Details",
                         font=("Arial", 18, "bold"), bg="white").pack()

                text = f"""
First name: {c.get_first_name()}
Last name: {c.get_last_name()}
Account No: {c.get_account_no()}

Address:
  {c.get_address()[0]}
  {c.get_address()[1]}
  {c.get_address()[2]}
  {c.get_address()[3]}

Account Type: {c.get_account_type()}
Balance: £{c.get_balance():.2f}
"""
                tk.Label(self.right_frame, text=text,
                         justify="left", bg="white",
                         font=("Arial", 12)).pack(pady=20)

        tk.Button(self.right_frame, text="Search", command=show).pack(pady=10)

    # ---------------- PRINT ALL ----------------
    def print_all(self):
        self.clear_right()

        canvas = tk.Canvas(self.right_frame, bg="white")
        scrollbar = tk.Scrollbar(self.right_frame, command=canvas.yview)
        frame = tk.Frame(canvas, bg="white")

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for c in self.system.accounts_list:
            box = tk.Frame(frame, bg="#f4f6f7", bd=1, relief="solid")
            box.pack(fill="x", padx=10, pady=5)

            text = f"""
First name: {c.get_first_name()}
Last name: {c.get_last_name()}
Account No: {c.get_account_no()}

Address:
  {c.get_address()[0]}
  {c.get_address()[1]}
  {c.get_address()[2]}
  {c.get_address()[3]}

Account Type: {c.get_account_type()}
Balance: £{c.get_balance():.2f}
"""
            tk.Label(box, text=text, justify="left",
                     bg="#f4f6f7").pack(padx=10, pady=10)

    # ---------------- UPDATE CUSTOMER ----------------
    def update_customer(self):
        self.clear_right()

        tk.Label(self.right_frame, text="Update Customer",
                 font=("Arial", 18), bg="white").pack()

        fields = ["Last Name", "New First Name", "New Last Name",
                  "House", "Street", "City", "Postcode"]

        entries = {}
        for f in fields:
            tk.Label(self.right_frame, text=f, bg="white").pack()
            e = tk.Entry(self.right_frame)
            e.pack()
            entries[f] = e

        def update():
            c = self.system.search_customers_by_name(entries["Last Name"].get())
            if c:
                c.update_first_name(entries["New First Name"].get())
                c.update_last_name(entries["New Last Name"].get())
                c.update_address([
                    entries["House"].get(),
                    entries["Street"].get(),
                    entries["City"].get(),
                    entries["Postcode"].get()
                ])
                self.system.save_customers_to_file()
                messagebox.showinfo("Success", "Updated Successfully")

        tk.Button(self.right_frame, text="Update", command=update).pack(pady=10)

    # ---------------- DELETE ----------------
    def delete_customer(self):
        self.clear_right()

        tk.Label(self.right_frame, text="Delete Customer",
                 font=("Arial", 18), bg="white").pack()

        e = tk.Entry(self.right_frame)
        e.pack()

        def delete():
            c = self.system.search_customers_by_name(e.get())
            if c:
                self.system.accounts_list.remove(c)
                self.system.save_customers_to_file()
                messagebox.showinfo("Deleted", "Customer removed")

        tk.Button(self.right_frame, text="Delete", command=delete).pack()

    # ---------------- CREATE CUSTOMER ----------------
    def create_customer(self):
        self.clear_right()

        fields = ["First Name", "Last Name", "Balance",
                  "House", "Street", "City", "Postcode"]

        entries = {}
        for f in fields:
            tk.Label(self.right_frame, text=f, bg="white").pack()
            e = tk.Entry(self.right_frame)
            e.pack()
            entries[f] = e

        acc_type = ttk.Combobox(self.right_frame, values=["Savings", "Advanced"])
        acc_type.pack()

        def create():
            acc_no = self.system.generate_account_number()

            if acc_type.get() == "Savings":
                c = SavingsAccount(entries["First Name"].get(),
                                   entries["Last Name"].get(),
                                   [entries["House"].get(),
                                    entries["Street"].get(),
                                    entries["City"].get(),
                                    entries["Postcode"].get()],
                                   acc_no,
                                   float(entries["Balance"].get()), 0.05)
            else:
                c = AdvancedAccount(entries["First Name"].get(),
                                    entries["Last Name"].get(),
                                    [entries["House"].get(),
                                     entries["Street"].get(),
                                     entries["City"].get(),
                                     entries["Postcode"].get()],
                                    acc_no,
                                    float(entries["Balance"].get()), 500)

            self.system.accounts_list.append(c)
            self.system.save_customers_to_file()
            messagebox.showinfo("Success", "Customer Created")

        tk.Button(self.right_frame, text="Create", command=create).pack(pady=10)

    # ---------------- ADMIN ----------------
    def view_admin(self):
        self.clear_right()

        text = f"""
Username: {self.admin.get_username()}
First Name: {self.admin.get_first_name()}
Last Name: {self.admin.get_last_name()}
"""
        tk.Label(self.right_frame, text=text,
                 bg="white", font=("Arial", 14)).pack(pady=20)

    def update_admin(self):
        self.clear_right()

        tk.Label(self.right_frame, text="Update Admin", bg="white").pack()

        fname = tk.Entry(self.right_frame)
        fname.pack()
        lname = tk.Entry(self.right_frame)
        lname.pack()

        def update():
            self.admin.update_first_name(fname.get())
            self.admin.update_last_name(lname.get())
            messagebox.showinfo("Updated", "Admin updated")

        tk.Button(self.right_frame, text="Update", command=update).pack()

    # ---------------- REPORT ----------------
    def report(self):
        self.clear_right()

        total = sum(c.get_balance() for c in self.system.accounts_list)
        count = len(self.system.accounts_list)

        text = f"""
Total Customers: {count}
Total Balance: £{total:.2f}
"""
        tk.Label(self.right_frame, text=text,
                 font=("Arial", 16), bg="white").pack(pady=20)


if __name__ == "__main__":
    BankGUI()

