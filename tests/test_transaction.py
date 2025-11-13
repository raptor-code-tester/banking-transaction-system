import pytest 
import sys
import pathlib
from decimal import Decimal

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src.transaction import TransactionType, TransactionStatus, Transaction, Account


def test_hello_world():
    assert "Hello World" == "Hello World"


def test_transaction_initialization_and_completion():
    """Test that a Transaction is properly initialized and can be completed."""
    # Arrange
    account_id = "ACC123"
    amount = Decimal("100.00")
    transaction_type = TransactionType.DEPOSIT
    description = "Test deposit"
    
    # Act
    transaction = Transaction(account_id, amount, transaction_type, description)
    
    # Assert - Check initial state
    assert transaction.account_id == account_id
    assert transaction.amount == amount
    assert transaction.transaction_type == transaction_type
    assert transaction.description == description
    assert transaction.status == TransactionStatus.PENDING
    assert transaction.id is not None
    assert transaction.timestamp is not None
    
    # Act - Complete the transaction
    transaction.complete()
    
    # Assert - Check completed state
    assert transaction.status == TransactionStatus.COMPLETED
