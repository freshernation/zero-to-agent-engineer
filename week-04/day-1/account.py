"""BankAccount(owner, balance=0)

    .owner  .balance    attributes
    deposit(amount)     adds; raises ValueError("Deposit must be positive") for <= 0
    withdraw(amount)    subtracts; raises ValueError("Insufficient funds")
    can_afford(amount)  True/False, changes nothing

A refused deposit or withdrawal must leave the balance exactly as it was.
"""
