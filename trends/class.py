class Account:
    interest = 0.02

    #                   name
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance -= amount
        return self.balance


class CheckingAccount(Account):
    withdraw_change = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_change)


class SavingsAccount(Account):
    deposit_charge = 2

    def deposit(self, amount):
        return Account.deposit(self, amount - self.deposit_charge)


class AsSeenOnTVAccount(CheckingAccount, SavingsAccount):
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 1  # a free dollar

such_a_deal = AsSeenOnTVAccount("John")
such_a_deal.deposit(20)   # $2 fee from SavingsAccount.deposit
such_a_deal.withdraw(5)   # $1 fee from CheckingAccount.withdraw