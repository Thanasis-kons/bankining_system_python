import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, first_name, last_name, vat_number):
        self.first_name = first_name
        self.last_name = last_name
        self.vat_number = vat_number
        self.bank_accounts = []

class BankAccount:
    def __init__(self, account_number, available_amount, user):
        self.account_number = account_number
        self.available_amount = available_amount
        self.user = user

class BankAccountManagementSystemGUI:
    def __init__(self, root):
        self.root = root
        self.users = []

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.users_listbox = tk.Listbox(self.main_frame)
        self.users_listbox.pack(side=tk.LEFT, padx=15)

        self.load_users()

        self.view_button = tk.Button(
            self.main_frame, text="Bank Accounts", command=self.view_bank_accounts
        )
        self.view_button.pack(pady=5)

        self.create_button = tk.Button(
            self.main_frame, text="Bank Account Creation", command=self.create_bank_account
        )
        self.create_button.pack(pady=5)

        self.create_user_button = tk.Button(
            self.main_frame, text="New User Creation", command=self.create_new_user
        )
        self.create_user_button.pack(pady=5)

        self.delete_user_button = tk.Button(
            self.main_frame, text="Delete User", command=self.delete_user
        )
        self.delete_user_button.pack(pady=5)

        self.root.mainloop()

    def load_users(self):
        # Create some sample users and bank accounts
        user1 = User("John", "Doe", "123456")
        user1.bank_accounts.append(BankAccount("123", 1000, user1))
        user1.bank_accounts.append(BankAccount("456", 2000, user1))

        user2 = User("Mary", "Jones", "654321")
        user2.bank_accounts.append(BankAccount("789", 500, user2))

        self.users = [user1, user2]

        # Display users in the listbox
        self.update_users_listbox()

    def update_users_listbox(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.users:
            self.users_listbox.insert(tk.END, f"{user.first_name} {user.last_name} ({user.vat_number})")

        self.users_listbox.config(width=40)  # Set the width of the listbox widget

    def view_bank_accounts(self):
        selected_user_index = self.users_listbox.curselection()
        if not selected_user_index:
            messagebox.showinfo("Error", "Please select an account.")
            return

        selected_user = self.users[selected_user_index[0]]

        bank_accounts_window = tk.Toplevel(self.root)
        bank_accounts_window.title("Bank Accounts")

        bank_accounts_frame = tk.Frame(bank_accounts_window)
        bank_accounts_frame.pack()

        bank_accounts_listbox = tk.Listbox(bank_accounts_frame, width=30)
        bank_accounts_listbox.pack(side=tk.LEFT, padx=10)
        bank_accounts_listbox.config(width=50)
        for account in selected_user.bank_accounts:
            bank_accounts_listbox.insert(
                tk.END, f"Account: {account.account_number}, Available amount: {account.available_amount}"
            )

        deposit_button = tk.Button(
            bank_accounts_frame,
            text="Deposit",
            command=lambda: self.deposit_funds(selected_user, bank_accounts_listbox),
        )
        deposit_button.pack(pady=5)

        withdrawal_button = tk.Button(
            bank_accounts_frame,
            text="Withdrawal",
            command=lambda: self.withdraw_funds(selected_user, bank_accounts_listbox),
        )
        withdrawal_button.pack(pady=5)

        transfer_button = tk.Button(
            bank_accounts_frame,
            text="Transfer",
            command=lambda: self.transfer_funds(selected_user, bank_accounts_listbox),
        )
        transfer_button.pack(pady=5)

        delete_account_button = tk.Button(
            bank_accounts_frame,
            text="Delete Account",
            command=lambda: self.delete_account(selected_user, bank_accounts_listbox),
        )
        delete_account_button.pack(pady=5)

    def create_bank_account(self):
        selected_user_index = self.users_listbox.curselection()
        if not selected_user_index:
            messagebox.showinfo("Error", "Please select a user")
            return

        selected_user = self.users[selected_user_index[0]]

        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Bank Account Creation")

        account_number_label = tk.Label(create_account_window, text="Account Number:")
        account_number_label.pack()

        account_number_entry = tk.Entry(create_account_window)
        account_number_entry.pack()

        amount_label = tk.Label(create_account_window, text="Amount:")
        amount_label.pack()

        amount_entry = tk.Entry(create_account_window)
        amount_entry.pack()

        create_button = tk.Button(
            create_account_window,
            text="Create",
            command=lambda: self.add_bank_account(
                selected_user, account_number_entry.get(), amount_entry.get(), create_account_window
            ),
        )
        create_button.pack(pady=5)

    def deposit_funds(self, user, bank_accounts_listbox):
        selected_account_index = bank_accounts_listbox.curselection()
        if not selected_account_index:
            messagebox.showinfo("Error", "Please select a bank account.")
            return

        selected_account = user.bank_accounts[selected_account_index[0]]

        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Money Deposit")

        amount_label = tk.Label(deposit_window, text="Amount:")
        amount_label.pack()

        amount_entry = tk.Entry(deposit_window)
        amount_entry.pack()

        deposit_button = tk.Button(
            deposit_window,
            text="Deposit",
            command=lambda: self.update_balance(
                selected_account, amount_entry.get(), deposit_window, "deposit"
            ),
        )
        deposit_button.pack(pady=5)

    def withdraw_funds(self, user, bank_accounts_listbox):
        selected_account_index = bank_accounts_listbox.curselection()
        if not selected_account_index:
            messagebox.showinfo("Error", "Please select a bank account.")
            return

        selected_account = user.bank_accounts[selected_account_index[0]]

        withdrawal_window = tk.Toplevel(self.root)
        withdrawal_window.title("Amount Withdraw")

        amount_label = tk.Label(withdrawal_window, text="Amount:")
        amount_label.pack()

        amount_entry = tk.Entry(withdrawal_window)
        amount_entry.pack()

        withdrawal_button = tk.Button(
            withdrawal_window,
            text="Withdraw",
            command=lambda: self.update_balance(
                selected_account, amount_entry.get(), withdrawal_window, "withdraw"
            ),
        )
        withdrawal_button.pack(pady=5)

    def add_bank_account(self, user, account_number, amount, window):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showinfo("Error", "Invalid amount.")
            return

        new_account = BankAccount(account_number, amount, user)
        user.bank_accounts.append(new_account)

        messagebox.showinfo("Success", "The Bank Account was successfully created.")
        window.destroy()

    def create_new_user(self):
        create_user_window = tk.Toplevel(self.root)
        create_user_window.title("New User Creation")

        first_name_label = tk.Label(create_user_window, text="First Name:")
        first_name_label.pack()

        first_name_entry = tk.Entry(create_user_window)
        first_name_entry.pack()

        last_name_label = tk.Label(create_user_window, text="Last Name:")
        last_name_label.pack()

        last_name_entry = tk.Entry(create_user_window)
        last_name_entry.pack()

        vat_number_label = tk.Label(create_user_window, text="Tax Number:")
        vat_number_label.pack()

        vat_number_entry = tk.Entry(create_user_window)
        vat_number_entry.pack()

        account_number_label = tk.Label(create_user_window, text="Account Number:")
        account_number_label.pack()

        account_number_entry = tk.Entry(create_user_window)
        account_number_entry.pack()

        amount_label = tk.Label(create_user_window, text="Initial Deposit:")
        amount_label.pack()

        amount_entry = tk.Entry(create_user_window)
        amount_entry.pack()

        create_button = tk.Button(
            create_user_window,
            text="Create",
            command=lambda: self.add_new_user(
                first_name_entry.get(),
                last_name_entry.get(),
                vat_number_entry.get(),
                account_number_entry.get(),
                amount_entry.get(),
                create_user_window,
            ),
        )
        create_button.pack(pady=5)

    def add_new_user(self, first_name, last_name, vat_number, account_number, amount, window):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showinfo("Error", "Invalid amount.")
            return

        new_user = User(first_name, last_name, vat_number)
        new_account = BankAccount(account_number, amount, new_user)
        new_user.bank_accounts.append(new_account)
        self.users.append(new_user)

        messagebox.showinfo(
            "Success", "The new User and the bank account were successfully created."
        )
        self.update_users_listbox()
        window.destroy()

    def update_balance(self, account, amount, window, transaction_type):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showinfo("Error", "Invalid amount.")
            return

        if transaction_type == "withdraw" and amount > account.available_amount:
            messagebox.showinfo("Error", "Insufficient balance.")
            return

        if transaction_type == "deposit":
            account.available_amount += amount
        elif transaction_type == "withdraw":
            account.available_amount -= amount

        messagebox.showinfo(
            "Success", f"The transaction was completed. New balance: {account.available_amount}"
        )
        window.destroy()

    def delete_user(self):
        selected_user_index = self.users_listbox.curselection()
        if not selected_user_index:
            messagebox.showinfo("Error", "Please select a user.")
            return

        selected_user = self.users[selected_user_index[0]]

        # Check if any bank account of the user has available balance
        for account in selected_user.bank_accounts:
            if account.available_amount > 0:
                messagebox.showinfo(
                    "Error",
                    "Deletion of the user is not possible. The user still has bank accounts with a balance."
                )
                return

        confirmation = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete the user {selected_user.first_name} {selected_user.last_name}?"
        )
        if confirmation:
            self.users.remove(selected_user)
            messagebox.showinfo("Success", "The user was deleted successfully.")
            self.update_users_listbox()

    def delete_account(self, user, bank_accounts_listbox):
        selected_account_index = bank_accounts_listbox.curselection()
        if not selected_account_index:
            messagebox.showinfo("Error", "Please select a bank account.")
            return

        selected_account = user.bank_accounts[selected_account_index[0]]

        # Check if the selected account has available balance
        if selected_account.available_amount > 0:
            messagebox.showinfo(
                "Error",
                "Deletion of the account is not possible. The account still has a balance."
            )
            return

        confirmation = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete the account with number {selected_account.account_number}?"
        )
        if confirmation:
            user.bank_accounts.remove(selected_account)
            messagebox.showinfo("Success", "The bank account was deleted successfully.")
            self.view_bank_accounts()

    def transfer_funds(self, user, bank_accounts_listbox):
        selected_account_index = bank_accounts_listbox.curselection()
        if not selected_account_index:
            messagebox.showinfo("Error", "Please select a bank account.")
            return

        selected_account = user.bank_accounts[selected_account_index[0]]

        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Money Transfer")

        recipient_name_label = tk.Label(transfer_window, text="Recipient's Name:")
        recipient_name_label.pack()

        recipient_name_entry = tk.Entry(transfer_window)
        recipient_name_entry.pack()

        recipient_account_label = tk.Label(transfer_window, text="Recipient's Account Number:")
        recipient_account_label.pack()

        recipient_account_entry = tk.Entry(transfer_window)
        recipient_account_entry.pack()

        amount_label = tk.Label(transfer_window, text="Amount:")
        amount_label.pack()

        amount_entry = tk.Entry(transfer_window)
        amount_entry.pack()

        transfer_button = tk.Button(
            transfer_window,
            text="Transfer",
            command=lambda: self.transfer_amount(
                selected_account, recipient_name_entry.get(), recipient_account_entry.get(), amount_entry.get(),
                transfer_window
            ),
        )
        transfer_button.pack(pady=5)

    def transfer_amount(self, sender_account, recipient_name, recipient_account, amount, window):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showinfo("Error", "Invalid amount.")
            return

        # Find the recipient user and account
        recipient_user = None
        recipient_user_account = None
        for user in self.users:
            for account in user.bank_accounts:
                if account.account_number == recipient_account:
                    recipient_user = user
                    recipient_user_account = account
                    break

        if not recipient_user or not recipient_user_account:
            messagebox.showinfo("Error", "Recipient not found.")
            return

        confirmation = messagebox.askyesno(
            "Transfer Confirmation",
            f"Are you sure you want to transfer the amount {amount} from account {sender_account.account_number} "
            f"to account {recipient_user_account.account_number}?"
        )
        if confirmation:
            if amount > sender_account.available_amount:
                messagebox.showinfo("Error", "Insufficient balance.")
                return

            sender_account.available_amount -= amount
            recipient_user_account.available_amount += amount

            messagebox.showinfo("Success", "The transfer was completed successfully.")
            window.destroy()
            self.view_bank_accounts()

root = tk.Tk()
root.title("Bank Account Management System")
BankAccountManagementSystemGUI(root)
