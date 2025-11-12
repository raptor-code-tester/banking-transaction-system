# Banking Transaction System

A simple Python-based banking transaction system that demonstrates account management and transaction processing.

## Features

- **Account Management**: Create accounts with initial balances
- **Transaction Types**: Support for deposits, withdrawals, transfers, and payments
- **Transaction Status Tracking**: Pending, completed, and failed status management
- **Transaction History**: Complete audit trail for all account activities
- **Error Handling**: Validation for insufficient funds and invalid amounts

## File Structure

```
starting_code/
├── transaction.py    # Core transaction and account classes
├── main.py          # Demo script with test data
└── README.md        # This file
```

## Classes

### TransactionType (Enum)
- `DEPOSIT`: Money added to account
- `WITHDRAWAL`: Money removed from account  
- `TRANSFER`: Money moved between accounts
- `PAYMENT`: Money sent to merchants/services

### TransactionStatus (Enum)
- `PENDING`: Transaction initiated but not processed
- `COMPLETED`: Transaction successfully processed
- `FAILED`: Transaction could not be completed

### Transaction
Represents a single financial transaction with:
- Unique ID (UUID)
- Account ID
- Amount (Decimal for precision)
- Transaction type and status
- Timestamp and description
- Optional recipient ID for transfers

### Account
Manages account balance and transaction history:
- `deposit(amount, description)`: Add money to account
- `withdraw(amount, description)`: Remove money from account
- `transfer(recipient_account, amount, description)`: Send money to another account

## Usage

### Basic Example

```python
from decimal import Decimal
from transaction import Account

# Create accounts
alice = Account("ACC001", Decimal('1000.00'))
bob = Account("ACC002", Decimal('500.00'))

# Perform transactions
alice.deposit(Decimal('200.00'), "Salary")
alice.transfer(bob, Decimal('150.00'), "Payment")
bob.withdraw(Decimal('100.00'), "ATM")

print(f"Alice balance: ${alice.balance}")
print(f"Bob balance: ${bob.balance}")
```

### Running the Demo

```bash
python main.py
```

The demo script creates multiple accounts and performs various transactions including:
- Salary deposits and payments
- Inter-account transfers
- Merchant payments
- Error handling demonstrations
- Transaction statistics

## Key Design Decisions

1. **Decimal Precision**: Uses `Decimal` type for accurate financial calculations
2. **Immutable Transactions**: Once created, transaction details cannot be modified
3. **Atomic Transfers**: Transfer operations update both accounts simultaneously
4. **UUID Tracking**: Each transaction gets a unique identifier
5. **Status Management**: Clear transaction lifecycle with status updates

## Error Handling

The system validates:
- Positive transaction amounts
- Sufficient account balance for withdrawals/transfers
- Account existence for transfers

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Future Enhancements

- Database persistence
- Multi-currency support
- Transaction fees and limits
- Account types (checking, savings, etc.)
- Interest calculations
- Transaction reversal capabilities