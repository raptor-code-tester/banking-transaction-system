from enum import Enum
from datetime import datetime
from decimal import Decimal
import uuid

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction:
    def __init__(self, account_id: str, amount: Decimal, transaction_type: TransactionType, 
                 description: str = "", recipient_id: str = None):
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.recipient_id = recipient_id
        self.timestamp = datetime.now()
        self.status = TransactionStatus.PENDING
    
    def complete(self):
        self.status = TransactionStatus.COMPLETED
    
    def fail(self):
        self.status = TransactionStatus.FAILED

class Account:
    def __init__(self, account_id: str, initial_balance: Decimal = Decimal('0')):
        self.account_id = account_id
        self.balance = initial_balance
        self.transactions = []
    
    def deposit(self, amount: Decimal, description: str = ""):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        transaction = Transaction(self.account_id, amount, TransactionType.DEPOSIT, description)
        self.balance += amount
        transaction.complete()
        self.transactions.append(transaction)
        return transaction
    
    def withdraw(self, amount: Decimal, description: str = ""):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        
        transaction = Transaction(self.account_id, amount, TransactionType.WITHDRAWAL, description)
        self.balance -= amount
        transaction.complete()
        self.transactions.append(transaction)
        return transaction
    
    def transfer(self, recipient_account, amount: Decimal, description: str = ""):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        
        # Debit from sender
        debit_tx = Transaction(self.account_id, amount, TransactionType.TRANSFER, 
                              f"Transfer to {recipient_account.account_id}: {description}", 
                              recipient_account.account_id)
        
        # Credit to recipient
        credit_tx = Transaction(recipient_account.account_id, amount, TransactionType.TRANSFER,
                               f"Transfer from {self.account_id}: {description}",
                               self.account_id)
        
        self.balance -= amount
        recipient_account.balance += amount
        
        debit_tx.complete()
        credit_tx.complete()
        
        self.transactions.append(debit_tx)
        recipient_account.transactions.append(credit_tx)
        
        return debit_tx, credit_tx
