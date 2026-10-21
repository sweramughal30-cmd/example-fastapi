from app.calculations import add,BankAccount,Insuuf_money
import pytest


@pytest.fixture
def zero_account_amount():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1,num2,expected",
    [(3,5,8),
    (5,5,10),
    (12,4,16)
])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected

def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50
def test_bank_default_amount(zero_account_amount):
    assert zero_account_amount.balance == 0
def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70
def test_bank_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,6 ) == 55

@pytest.mark.parametrize("deposited,withdrew,expected",
    [(200,100,100),
    (1200,100,1100),
    (500,100,400)
])
def test_bank_transaction(zero_account_amount,deposited,withdrew,expected):
    zero_account_amount.deposit(deposited)
    zero_account_amount.withdraw(withdrew)
    assert zero_account_amount.balance == expected
def test_insuuf_money(bank_account):
    with pytest.raises(Insuuf_money):
        bank_account.withdraw(60)


