# Consts

MENU = """

[d] Deposit
[w] Withdraw money
[s] Bank statement
[e] Exit

=> """

CURRENCY_IDENTIFIER = "R$"
WITHDRAW_LIMIT = 3

# Variables
account_balance = 0
limit_withdrawals = 500
withdraw_money = ""
amount_of_withdraws = 0

# Types
type Withdraw_Validations = {
    "is_valid": bool, 
    "exceeded_account_balance": bool, 
    "exceeded_limit": bool, 
    "exceeded_withdrawals": bool, 
    "value_withdraw_greater_than_zero": bool
}

type Withdraw_Result = {
    "account_balance":float, 
    "withdraw_money":str, 
    "amount_of_withdraws":int
}

type Deposit_Result = {
    "account_balance":float, 
    "withdraw_money":str,
    "error_message" :str
}

## Functions

def make_withdraw(*, param_account_balance, param_limit_withdrawals, param_amount_of_withdraws, param_withdraw_money) -> Withdraw_Result:
    """
    This function make a withdraw in customer's back account.

    Args:
        param_account_balance (float, keyword only): Current balance of the customer's account.
        param_limit_withdrawals (int, keyword only): Customer withdrawal limit
        param_amount_of_withdraws (int, keyword only): Customer withdrawals successfully completed.
        param_withdraw_money (str, keyword only): Description of the customer's withdrawal transaction.

    Returns:
        Withdraw_Result: Describes the important information needed during a customer's withdrawal transaction.
    """

    withdraw_results:Withdraw_Result = None

    value_input = float(input("Please provide the withdrawal amount: "))
    new_amount_of_withdraws = param_amount_of_withdraws + 1
    dict_withdraw_is_valid = withdraw_is_valid (
                                                 param_account_balance      = param_account_balance
                                                ,param_limit_withdrawals    = param_limit_withdrawals
                                                ,param_amount_of_withdraws  = new_amount_of_withdraws
                                                ,param_value_withdraw       = value_input 
                                                )

    if dict_withdraw_is_valid["exceeded_account_balance"]:
        print("Operation failed! You do not have sufficient account balance.")

    elif dict_withdraw_is_valid["exceeded_limit"]:
        print("The transaction failed! The withdrawal amount exceeds the limit.")

    elif dict_withdraw_is_valid["exceeded_withdrawals"]:
        print("Operation failed! Maximum number of withdrawals exceeded.")

    elif dict_withdraw_is_valid["value_withdraw_greater_than_zero"]:
        param_account_balance       -= value_input
        param_withdraw_money        += f"Withdraw money: {CURRENCY_IDENTIFIER} {value_input:.2f}\n"
        param_amount_of_withdraws   += 1

        withdraw_results = {"account_balance":param_account_balance, "withdraw_money":param_withdraw_money, "amount_of_withdraws":param_amount_of_withdraws}

    else:
        print("The operation failed! The value entered is invalid.")

    return withdraw_results


def withdraw_is_valid(*, param_account_balance, param_limit_withdrawals, param_amount_of_withdraws, param_value_withdraw) -> Withdraw_Validations:
    """
        This function make a withdraw in customer's back account.
        
        #### Validations:
        - is_exceeded_account_balance()
        - is_exceeded_limit()
        - is_exceeded_withdrawals()
        - is_value_withdraw_greater_than_zero()
        - is_valid

    Args:
        param_account_balance (float, keyword only): Current balance of the customer's account.
        param_limit_withdrawals (int, keyword only): Customer withdrawal limit
        param_amount_of_withdraws (int, keyword only): Customer withdrawals successfully completed.
        param_value_withdraw (float, keyword only): Withdrawal amount that the customer needs

    Returns:
        Withdraw_Validations: Consistency checks to allow the customer's withdrawal transaction to proceed.

    """    

    exceeded_account_balance = is_exceeded_account_balance(param_value_withdraw, param_account_balance)
    exceeded_limit = is_exceeded_limit(param_value_withdraw , limit_withdrawals)
    exceeded_withdrawals = is_exceeded_withdrawals (param_amount_of_withdraws, param_limit_withdrawals)
    value_withdraw_greater_than_zero  = is_value_withdraw_greater_than_zero(param_value_withdraw)
    is_valid = not exceeded_account_balance and not exceeded_limit and not exceeded_withdrawals and value_withdraw_greater_than_zero

    return {"is_valid": is_valid, "exceeded_account_balance": exceeded_account_balance, "exceeded_limit":exceeded_limit,  "exceeded_withdrawals":exceeded_withdrawals, "value_withdraw_greater_than_zero":value_withdraw_greater_than_zero}


def is_exceeded_account_balance (param_value_withdraw , param_account_balance) -> bool:
    """
    Verify if it is true that the withdrawal amount exceeds the account balance.

    Args:
        param_value_withdraw (float): Withdrawal amount that the customer needs
        param_account_balance (float): Current balance of the customer's account.

    Returns:
        bool: If the amount exceeds the account balance, the **True** value will be returned.
    """    
    return param_value_withdraw > param_account_balance


def is_exceeded_limit(param_value_withdraw , limit_withdrawals)-> bool:
    """
    Verify that the withdrawal amount is actually higher than the system's overall withdrawal limit.

    Args:
        param_value_withdraw (float): Withdrawal amount that the customer needs
        limit_withdrawals (float): Global system limit value. This value is passed as an argument because the function only validates the desired value against the constraint value.

    Returns:
        bool: If the amount exceeds the limit value, the **True** value will be returned.
    """    
    return param_value_withdraw > limit_withdrawals


def is_exceeded_withdrawals (param_amount_of_withdraws, param_withdraw_limit)-> bool:
    """
    Check if the number of withdrawals exceeds the limit allowed by the system.

    Args:
        param_amount_of_withdraws (int): Number of withdrawals (completed + desired) to date.
        param_withdraw_limit (int): The maximum number of withdrawals allowed by the system should be used as a criterion.

    Returns:
        bool: If the amount exceeds the limit value, the **True** value will be returned.
    """ 
    return param_amount_of_withdraws > param_withdraw_limit


def is_value_withdraw_greater_than_zero(param_value_withdraw)-> bool:
    """
    Check if the withdrawal transaction amount is greater than 0 (zero).

    Args:
        param_value_withdraw (int): Value of the withdrawal transaction.

    Returns:
        bool: If the withdrawal transaction value is greater than 0 (zero), True will be returned.
    """ 
    return param_value_withdraw > 0


def make_deposit(param_account_balance, param_withdraw_money, /) -> Deposit_Result:
    """
    This function make a deposit in customer's back account.

    Args:
        param_account_balance (float, keyword only): Current balance of the customer's account.
        param_withdraw_money (str, keyword only): Description of the customer's withdrawal transaction.

    Returns:
        Deposit_Result: Describes the important information needed during a customer's withdrawal transaction.
    """ 
    value_input = float(input("Please provide the deposit amount: "))

    account_balance = param_account_balance
    withdraw_money = param_withdraw_money
    error_message = ""

    if is_deposit_valid(value_input):
        account_balance += value_input
        withdraw_money += f"Deposit: {CURRENCY_IDENTIFIER} {value_input:.2f}\n"

    else:
        error_message = "The operation failed! The value entered is invalid."

    return {"account_balance": account_balance, "withdraw_money": withdraw_money, "error_message": error_message}


def is_deposit_valid(param_deposit_value) -> bool:
    """
    Check if the deposit transaction amount is greater than 0 (zero).

    Args:
        param_deposit_value (int): Value of the deposit transaction.

    Returns:
        bool: If the deposit transaction value is greater than 0 (zero), True will be returned.
    """ 

    return param_deposit_value > 0


## Main rotine
while True:

    option = input(MENU)

    if option == "d":
        result = make_deposit(account_balance, withdraw_money)

        if not result or len(result["error_message"]) > 1:
            print(result["error_message"])

        account_balance = result["account_balance"]
        withdraw_money = result["withdraw_money"]

    elif option == "w":
        result = make_withdraw(
             param_account_balance = account_balance 
            ,param_limit_withdrawals = WITHDRAW_LIMIT 
            ,param_amount_of_withdraws = amount_of_withdraws 
            ,param_withdraw_money = withdraw_money
            )
        
        if result is None: continue

        account_balance = result["account_balance"]
        withdraw_money  = result["withdraw_money"]
        amount_of_withdraws = result["amount_of_withdraws"]

    elif option == "s":
        print("\n================ withdraw_money ================")
        print("No transactions were carried out." if not withdraw_money else withdraw_money)
        print(f"\nAccount balance: {CURRENCY_IDENTIFIER} {account_balance:.2f}")
        print("==========================================")

    elif option == "e":
        break

    else:
        print("Invalid operation, please select the desired operation again.")
