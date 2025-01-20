import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


data = {
    "accounts": {}, 
    "transactions": [], 
    "admin_logs": [], 
    "interest_rates": {"savings": 0.05, "loan": 0.1}  
}


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# Helper Functions
def authenticate(account_number, password):
    account = data["accounts"].get(account_number)
    if account and account["password"] == password:
        return True
    return False

def register_account(account_number, name, password, email, phone, address):
    if account_number in data["accounts"]:
        return False 
    data["accounts"][account_number] = {
        "name": name,
        "balance": 0.0,  
        "password": password,
        "loans": 0.0, 
        "email": email,
        "phone": phone,
        "address": address
    }
    return True

def calculate_interest():
    for account_number, account in data["accounts"].items():
       
        savings_interest = account["balance"] * data["interest_rates"]["savings"]
        account["balance"] += savings_interest
        data["transactions"].append((account_number, "Savings Interest", savings_interest, datetime.now()))

   
        if account["loans"] > 0:
            loan_interest = account["loans"] * data["interest_rates"]["loan"]
            account["loans"] += loan_interest
            data["transactions"].append((account_number, "Loan Interest", loan_interest, datetime.now()))


class BankingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f8")

        self.main_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RIDGE, bd=5)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.current_user = None 
        self.theme = "light"  

        self.show_home_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Welcome to the Banking System", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        tk.Button(self.main_frame, text="Login", font=("Arial", 16), bg="#4CAF50", fg="#ffffff", command=self.show_login_screen).pack(pady=10)
        tk.Button(self.main_frame, text="Register", font=("Arial", 16), bg="#2196F3", fg="#ffffff", command=self.show_register_screen).pack(pady=10)
        tk.Button(self.main_frame, text="Admin Panel", font=("Arial", 16), bg="#FF9800", fg="#ffffff", command=self.show_admin_login_screen).pack(pady=10)
        tk.Button(self.main_frame, text="Exit", font=("Arial", 16), bg="#f44336", fg="#ffffff", command=self.root.quit).pack(pady=10)

    def show_login_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Account Login", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        tk.Label(self.main_frame, text="Account Number", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        account_number_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        account_number_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 14), relief=tk.GROOVE, bd=3)
        password_entry.pack(pady=5)

        def login():
            account_number = account_number_entry.get()
            password = password_entry.get()
            if authenticate(account_number, password):
                self.current_user = account_number 
                self.show_account_dashboard(account_number)
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.main_frame, text="Login", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=login).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#f44336", fg="#ffffff", command=self.show_home_screen).pack(pady=5)

    def show_register_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Account Registration", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        tk.Label(self.main_frame, text="Account Number", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        account_number_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        account_number_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Name", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        name_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 14), relief=tk.GROOVE, bd=3)
        password_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Email", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        email_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        email_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Phone", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        phone_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        phone_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Address", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        address_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        address_entry.pack(pady=5)

        def register():
            account_number = account_number_entry.get()
            name = name_entry.get()
            password = password_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            if register_account(account_number, name, password, email, phone, address):
                messagebox.showinfo("Success", "Account created successfully")
                self.show_home_screen()
            else:
                messagebox.showerror("Error", "Account already exists")

        tk.Button(self.main_frame, text="Register", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=register).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#f44336", fg="#ffffff", command=self.show_home_screen).pack(pady=5)

    def show_account_dashboard(self, account_number):
        self.clear_frame()

        account = data["accounts"].get(account_number)
        tk.Label(self.main_frame, text=f"Welcome, {account['name']}", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        balance_label = tk.Label(self.main_frame, text=f"Account Balance: ${account['balance']:.2f}", font=("Arial", 14), bg="#ffffff")
        balance_label.pack(pady=10)

        loan_label = tk.Label(self.main_frame, text=f"Outstanding Loan: ${account['loans']:.2f}", font=("Arial", 14), bg="#ffffff")
        loan_label.pack(pady=10)

        def deposit():
            try:
                amount = float(amount_entry.get())
                if account["loans"] > 0:
                    if amount <= account["loans"]:
                        account["loans"] -= amount
                    else:
                        account["balance"] += (amount - account["loans"])
                        account["loans"] = 0
                else:
                    account["balance"] += amount
                data["transactions"].append((account_number, "Deposit", amount, datetime.now()))
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
                self.show_account_dashboard(account_number)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered")

        def withdraw():
            try:
                amount = float(amount_entry.get())
                if account["balance"] >= amount:
                    account["balance"] -= amount
                    data["transactions"].append((account_number, "Withdrawal", amount, datetime.now()))
                    messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
                    self.show_account_dashboard(account_number)
                else:
                    messagebox.showerror("Error", "Insufficient balance")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered")

        def loan():
            try:
                loan_amount = float(amount_entry.get())
                account["loans"] += loan_amount
                data["transactions"].append((account_number, "Loan", loan_amount, datetime.now()))
                messagebox.showinfo("Success", f"Loan of ${loan_amount:.2f} granted")
                self.show_account_dashboard(account_number)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered")

        def repay_loan():
            try:
                repayment_amount = float(amount_entry.get())
                if account["loans"] > 0:
                    if repayment_amount <= account["loans"]:
                        account["loans"] -= repayment_amount
                        account["balance"] -= repayment_amount
                        data["transactions"].append((account_number, "Loan Repayment", repayment_amount, datetime.now()))
                        messagebox.showinfo("Success", f"Repaid ${repayment_amount:.2f} towards loan")
                    else:
                        messagebox.showerror("Error", "Repayment amount exceeds loan balance")
                else:
                    messagebox.showerror("Error", "No outstanding loan")
                self.show_account_dashboard(account_number)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered")

        def transfer_funds():
            recipient_account = simpledialog.askstring("Transfer Funds", "Enter recipient's account number:")
            if recipient_account in data["accounts"]:
                try:
                    transfer_amount = float(amount_entry.get())
                    if account["balance"] >= transfer_amount:
                        account["balance"] -= transfer_amount
                        data["accounts"][recipient_account]["balance"] += transfer_amount
                        data["transactions"].append((account_number, "Transfer Out", transfer_amount, datetime.now()))
                        data["transactions"].append((recipient_account, "Transfer In", transfer_amount, datetime.now()))
                        messagebox.showinfo("Success", f"Transferred ${transfer_amount:.2f} to {recipient_account}")
                    else:
                        messagebox.showerror("Error", "Insufficient balance")
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount entered")
            else:
                messagebox.showerror("Error", "Recipient account not found")

        def view_transactions():
            transactions_window = tk.Toplevel(self.root)
            transactions_window.title("Transaction History")

            tree = ttk.Treeview(transactions_window, columns=("Type", "Amount", "Timestamp"), show="headings")
            tree.heading("Type", text="Transaction Type")
            tree.heading("Amount", text="Amount")
            tree.heading("Timestamp", text="Timestamp")

            for acc_no, txn_type, amount, timestamp in data["transactions"]:
                if acc_no == account_number:
                    tree.insert("", "end", values=(txn_type, amount, timestamp))

            tree.pack(fill="both", expand=True)

        def update_details():
            update_window = tk.Toplevel(self.root)
            update_window.title("Update Details")

            tk.Label(update_window, text="Email", font=("Arial", 14)).pack(pady=5)
            email_entry = tk.Entry(update_window, font=("Arial", 14), relief=tk.GROOVE, bd=3)
            email_entry.insert(0, account["email"])
            email_entry.pack(pady=5)

            tk.Label(update_window, text="Phone", font=("Arial", 14)).pack(pady=5)
            phone_entry = tk.Entry(update_window, font=("Arial", 14), relief=tk.GROOVE, bd=3)
            phone_entry.insert(0, account["phone"])
            phone_entry.pack(pady=5)

            tk.Label(update_window, text="Address", font=("Arial", 14)).pack(pady=5)
            address_entry = tk.Entry(update_window, font=("Arial", 14), relief=tk.GROOVE, bd=3)
            address_entry.insert(0, account["address"])
            address_entry.pack(pady=5)

            def save_changes():
                account["email"] = email_entry.get()
                account["phone"] = phone_entry.get()
                account["address"] = address_entry.get()
                messagebox.showinfo("Success", "Details updated successfully")
                update_window.destroy()

            tk.Button(update_window, text="Save", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=save_changes).pack(pady=10)

        def change_password():
            new_password = simpledialog.askstring("Change Password", "Enter new password:", show="*")
            if new_password:
                account["password"] = new_password
                messagebox.showinfo("Success", "Password changed successfully")

        def logout():
            self.current_user = None 
            self.show_home_screen()

        tk.Label(self.main_frame, text="Amount", font=("Arial", 14), bg="#ffffff").pack(pady=10)
        amount_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        amount_entry.pack(pady=5)

        tk.Button(self.main_frame, text="Deposit", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=deposit).pack(pady=10)
        tk.Button(self.main_frame, text="Withdraw", font=("Arial", 14), bg="#2196F3", fg="#ffffff", command=withdraw).pack(pady=10)
        tk.Button(self.main_frame, text="Apply for Loan", font=("Arial", 14), bg="#FF9800", fg="#ffffff", command=loan).pack(pady=10)
        tk.Button(self.main_frame, text="Repay Loan", font=("Arial", 14), bg="#FF5722", fg="#ffffff", command=repay_loan).pack(pady=10)
        tk.Button(self.main_frame, text="Transfer Funds", font=("Arial", 14), bg="#9C27B0", fg="#ffffff", command=transfer_funds).pack(pady=10)
        tk.Button(self.main_frame, text="View Transactions", font=("Arial", 14), bg="#607D8B", fg="#ffffff", command=view_transactions).pack(pady=10)
        tk.Button(self.main_frame, text="Update Details", font=("Arial", 14), bg="#3F51B5", fg="#ffffff", command=update_details).pack(pady=10)
        tk.Button(self.main_frame, text="Change Password", font=("Arial", 14), bg="#E91E63", fg="#ffffff", command=change_password).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", font=("Arial", 14), bg="#f44336", fg="#ffffff", command=logout).pack(pady=10)

    def show_admin_login_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Admin Login", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        tk.Label(self.main_frame, text="Username", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        username_entry = tk.Entry(self.main_frame, font=("Arial", 14), relief=tk.GROOVE, bd=3)
        username_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password", font=("Arial", 14), bg="#ffffff").pack(pady=5)
        password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 14), relief=tk.GROOVE, bd=3)
        password_entry.pack(pady=5)

        def admin_login():
            username = username_entry.get()
            password = password_entry.get()
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")

        tk.Button(self.main_frame, text="Login", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=admin_login).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#f44336", fg="#ffffff", command=self.show_home_screen).pack(pady=5)

    def show_admin_dashboard(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), fg="#333333", bg="#ffffff").pack(pady=20)

        def view_all_accounts():
            accounts_window = tk.Toplevel(self.root)
            accounts_window.title("All Accounts")

            tree = ttk.Treeview(accounts_window, columns=("Account", "Name", "Balance", "Loans"), show="headings")
            tree.heading("Account", text="Account Number")
            tree.heading("Name", text="Name")
            tree.heading("Balance", text="Balance")
            tree.heading("Loans", text="Loans")

            for acc_no, details in data["accounts"].items():
                tree.insert("", "end", values=(acc_no, details["name"], details["balance"], details["loans"]))

            tree.pack(fill="both", expand=True)

        def view_all_transactions():
            transactions_window = tk.Toplevel(self.root)
            transactions_window.title("All Transactions")

            tree = ttk.Treeview(transactions_window, columns=("Account", "Type", "Amount", "Timestamp"), show="headings")
            tree.heading("Account", text="Account Number")
            tree.heading("Type", text="Transaction Type")
            tree.heading("Amount", text="Amount")
            tree.heading("Timestamp", text="Timestamp")

            for acc_no, txn_type, amount, timestamp in data["transactions"]:
                tree.insert("", "end", values=(acc_no, txn_type, amount, timestamp))

            tree.pack(fill="both", expand=True)

        def freeze_account():
            account_number = simpledialog.askstring("Freeze Account", "Enter account number to freeze:")
            if account_number in data["accounts"]:
                data["accounts"][account_number]["frozen"] = True
                messagebox.showinfo("Success", f"Account {account_number} frozen")
            else:
                messagebox.showerror("Error", "Account not found")

        def unfreeze_account():
            account_number = simpledialog.askstring("Unfreeze Account", "Enter account number to unfreeze:")
            if account_number in data["accounts"]:
                data["accounts"][account_number]["frozen"] = False
                messagebox.showinfo("Success", f"Account {account_number} unfrozen")
            else:
                messagebox.showerror("Error", "Account not found")

        def send_notification():
            account_number = simpledialog.askstring("Send Notification", "Enter account number:")
            if account_number in data["accounts"]:
                message = simpledialog.askstring("Send Notification", "Enter message:")
                if message:
                    data["transactions"].append((account_number, "Notification", 0, datetime.now()))
                    messagebox.showinfo("Success", f"Notification sent to {account_number}")
            else:
                messagebox.showerror("Error", "Account not found")

        def manage_interest_rates():
            rates_window = tk.Toplevel(self.root)
            rates_window.title("Manage Interest Rates")

            tk.Label(rates_window, text="Savings Interest Rate", font=("Arial", 14)).pack(pady=5)
            savings_rate_entry = tk.Entry(rates_window, font=("Arial", 14), relief=tk.GROOVE, bd=3)
            savings_rate_entry.insert(0, data["interest_rates"]["savings"])
            savings_rate_entry.pack(pady=5)

            tk.Label(rates_window, text="Loan Interest Rate", font=("Arial", 14)).pack(pady=5)
            loan_rate_entry = tk.Entry(rates_window, font=("Arial", 14), relief=tk.GROOVE, bd=3)
            loan_rate_entry.insert(0, data["interest_rates"]["loan"])
            loan_rate_entry.pack(pady=5)

            def save_rates():
                try:
                    data["interest_rates"]["savings"] = float(savings_rate_entry.get())
                    data["interest_rates"]["loan"] = float(loan_rate_entry.get())
                    messagebox.showinfo("Success", "Interest rates updated successfully")
                    rates_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid interest rate")

            tk.Button(rates_window, text="Save", font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=save_rates).pack(pady=10)

        def view_audit_logs():
            logs_window = tk.Toplevel(self.root)
            logs_window.title("Audit Logs")

            tree = ttk.Treeview(logs_window, columns=("Action", "Timestamp"), show="headings")
            tree.heading("Action", text="Action")
            tree.heading("Timestamp", text="Timestamp")

            for action, timestamp in data["admin_logs"]:
                tree.insert("", "end", values=(action, timestamp))

            tree.pack(fill="both", expand=True)

        def show_analytics():
            analytics_window = tk.Toplevel(self.root)
            analytics_window.title("Analytics Dashboard")

            total_deposits = sum(amount for _, txn_type, amount, _ in data["transactions"] if txn_type == "Deposit")
            total_loans = sum(amount for _, txn_type, amount, _ in data["transactions"] if txn_type == "Loan")
            total_accounts = len(data["accounts"])

            fig, ax = plt.subplots(1, 2, figsize=(10, 5))
            ax[0].bar(["Total Deposits", "Total Loans", "Total Accounts"], [total_deposits, total_loans, total_accounts])
            ax[0].set_title("Key Metrics")

            account_balances = [account["balance"] for account in data["accounts"].values()]
            ax[1].pie(account_balances, labels=data["accounts"].keys(), autopct="%1.1f%%")
            ax[1].set_title("Account Balances")

            canvas = FigureCanvasTkAgg(fig, master=analytics_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(self.main_frame, text="View All Accounts", font=("Arial", 14), bg="#2196F3", fg="#ffffff", command=view_all_accounts).pack(pady=10)
        tk.Button(self.main_frame, text="View All Transactions", font=("Arial", 14), bg="#607D8B", fg="#ffffff", command=view_all_transactions).pack(pady=10)
        tk.Button(self.main_frame, text="Freeze Account", font=("Arial", 14), bg="#FF5722", fg="#ffffff", command=freeze_account).pack(pady=10)
        tk.Button(self.main_frame, text="Unfreeze Account", font=("Arial", 14), bg="#E91E63", fg="#ffffff", command=unfreeze_account).pack(pady=10)
        tk.Button(self.main_frame, text="Send Notification", font=("Arial", 14), bg="#9C27B0", fg="#ffffff", command=send_notification).pack(pady=10)
        tk.Button(self.main_frame, text="Manage Interest Rates", font=("Arial", 14), bg="#3F51B5", fg="#ffffff", command=manage_interest_rates).pack(pady=10)
        tk.Button(self.main_frame, text="View Audit Logs", font=("Arial", 14), bg="#795548", fg="#ffffff", command=view_audit_logs).pack(pady=10)
        tk.Button(self.main_frame, text="Show Analytics", font=("Arial", 14), bg="#009688", fg="#ffffff", command=show_analytics).pack(pady=10)
        tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#f44336", fg="#ffffff", command=self.show_home_screen).pack(pady=10)

# Run the App
root = tk.Tk()
app = BankingSystem(root)
root.mainloop()
