import pytest 
import sys
import pathlib
from decimal import Decimal

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src.transaction import TransactionType, TransactionStatus, Transaction, Account


def test_hello_world():
    assert "Hello World" == "Hello World"


def test_transaction_creation():
    """Test that a Transaction is created with correct initial values"""
    account_id = "ACC123"
    amount = Decimal("100.50")
    transaction_type = TransactionType.DEPOSIT
    description = "Initial deposit"
    
    transaction = Transaction(account_id, amount, transaction_type, description)
    
    assert transaction.account_id == account_id
    assert transaction.amount == amount
    assert transaction.transaction_type == transaction_type
    assert transaction.description == description
    assert transaction.status == TransactionStatus.PENDING
    assert transaction.id is not None
    assert transaction.timestamp is not None
