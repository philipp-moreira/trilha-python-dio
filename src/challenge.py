# Consts

MENU = """

[c] Create new Customer
[d] Deposit
[w] Withdraw money
[s] Bank statement
[e] Exit

=> """

CURRENCY_IDENTIFIER = "R$"
WITHDRAW_LIMIT = 3
VALUE_LIMIT_WALDRAWALAS = 500


# Types
type Withdraw_Validations = {
    "is_valid": bool, 
    "exceeded_account_balance": bool, 
    "exceeded_limit": bool, 
    "exceeded_withdrawals": bool, 
    "value_withdraw_greater_than_zero": bool
}

type Result_Withdraw_Customer = {
    "customers": [Customer], 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Deposit_Customer = {
    "customers": [Customer], 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Address = {
    "street": str, 
    "number": str,
    "neighborhood": str,    
    "city": str,    
    "state": str
}

type Customer = {
    "name": str,
    "birth_date": str,
    "cpf": str,
    "account_balance": float,
    "withdraw_money": str,
    "amount_of_withdraws": int, 
    "limit_withdrawals": int,
    "value_limit_waldrawalas": int,
    "address": Address 
}

type Customers = [Customer]

type Result_Create_Customer = {
    "customer":Customer, 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Search_Customer = {
    "customer":Customer, 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Create_Address = {
    "address":Address, 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Register_Customer = {
    "customers": [Customer], 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Update_Customer = {
    "customers": [Customer], 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Result_Make_Customer = {
    "customers": [Customer], 
    "new_customer": Customer, 
    "success": bool, 
    "error_messages":[Business_Domain_Errors]
}

type Business_Domain_Errors = {
    "data": str,
    "error_messages": [str],
}

type  Characters_To_Replace= {
    "k_searched_character": str,
    "v_substitute_character": str,
}


# Variables
customers_bank = []

## Functions

def make_withdraw(*, param_customer, param_customers) -> Result_Withdraw_Customer:
    """
    This function make a withdraw in customer's back account.

    Args:
        param_account_balance (float, keyword only): Current balance of the customer's account.
        param_limit_withdrawals (int, keyword only): Customer withdrawal limit
        param_amount_of_withdraws (int, keyword only): Customer withdrawals successfully completed.
        param_withdraw_money (str, keyword only): Description of the customer's withdrawal transaction.

    Returns:
        Result_Withdraw_Customer: Describes the important information needed during a customer's withdrawal transaction.
    """

    customer = param_customer.copy()
    customers = param_customers.copy()
    errors_list = []
    withdraw_results:Result_Withdraw_Customer = None

    value_input = float(input("Please provide the withdrawal amount: "))

    new_amount_of_withdraws = customer["amount_of_withdraws"] + 1

    withdraw_is_valid_result = withdraw_is_valid (  param_account_balance               = customer["account_balance"]
                                                    ,param_limit_withdrawals            = customer["limit_withdrawals"]
                                                    ,param_amount_of_withdraws          = new_amount_of_withdraws
                                                    ,param_value_limit_to_waldrawalas   = customer["value_limit_waldrawalas"]
                                                    ,param_value_withdraw               = value_input 
                                                )

    if withdraw_is_valid_result["exceeded_account_balance"]:
        errors_list.append("Operation failed! You do not have sufficient account balance.")

    if withdraw_is_valid_result["exceeded_limit"]:
        errors_list.append("The transaction failed! The withdrawal amount exceeds the limit.")

    if withdraw_is_valid_result["exceeded_withdrawals"]:
        errors_list.append("Operation failed! Maximum number of withdrawals exceeded.")
    
    if not withdraw_is_valid_result["value_withdraw_greater_than_zero"]:
        errors_list.append("The operation failed! The value entered is invalid.")

    if len(errors_list) > 0:
        withdraw_results = {"customers": customers, "success": False, "error_messages": errors_list}

    else:
        customer["amount_of_withdraws"]   = new_amount_of_withdraws
        customer["account_balance"]       += (abs(value_input) * -1)
        customer["withdraw_money"]        += f"Withdraw money: {CURRENCY_IDENTIFIER} {value_input:.2f}\n"

        update_customer_result = update_customer(customer, customers)

        if not update_customer_result["success"]:
            errors_list.append(update_customer_result["error_message"])
            withdraw_results = {"customers": customers, "success": False, "error_messages": errors_list}

        else:
            withdraw_results = {"customers": update_customer_result["customers"], "success": True, "error_messages": errors_list}


    return withdraw_results


def withdraw_is_valid(*, param_account_balance, param_limit_withdrawals, param_amount_of_withdraws, param_value_limit_to_waldrawalas, param_value_withdraw) -> Withdraw_Validations:
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
        param_value_limit_to_waldrawalas (float, keyword only): Customer's value limit to waldrawalas.
        param_value_withdraw (float, keyword only): Withdrawal amount that the customer needs

    Returns:
        Withdraw_Validations: Consistency checks to allow the customer's withdrawal transaction to proceed.
    """    

    exceeded_account_balance = is_exceeded_account_balance(param_value_withdraw, param_account_balance)
    exceeded_limit = is_exceeded_limit(param_value_withdraw , param_value_limit_to_waldrawalas)
    exceeded_withdrawals = is_exceeded_withdrawals (param_amount_of_withdraws, param_limit_withdrawals)
    value_withdraw_greater_than_zero  = is_value_withdraw_greater_than_zero(param_value_withdraw)
    is_valid = not exceeded_account_balance and not exceeded_limit and not exceeded_withdrawals and value_withdraw_greater_than_zero

    return {"is_valid": is_valid, "exceeded_account_balance": exceeded_account_balance, "exceeded_limit": exceeded_limit, "exceeded_withdrawals": exceeded_withdrawals, "value_withdraw_greater_than_zero": value_withdraw_greater_than_zero}


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


def make_deposit(param_customer: Customer, param_customers: Customers, /) -> Result_Deposit_Customer:
    """
    This function make a deposit in customer's back account.

    Args:
        param_account_balance (float, keyword only): Current balance of the customer's account.
        param_withdraw_money (str, keyword only): Description of the customer's withdrawal transaction.

    Returns:
        Result_Deposit_Customer: Describes the important information needed during a customer's withdrawal transaction.
    """ 

    customer = param_customer.copy()
    customers = param_customers.copy()

    value_input = float(input("Please provide the deposit amount: "))
    errors_list = []
    update_customer_result :Result_Deposit_Customer= None

    if not is_deposit_valid(value_input):
        errors_list.append("The operation failed! The value entered is invalid.")
        update_customer_result = {"customers": customers, "success": False, "error_message": errors_list}

    else:
        customer["account_balance"]         += abs(value_input)
        customer["withdraw_money"]          += f"Deposit: {CURRENCY_IDENTIFIER} {value_input:.2f}\n"

        update_customer_result = update_customer(customer, customers)

        if not update_customer_result["success"]:
            errors_list.append(update_customer_result["error_message"])
            update_customer_result = {"customers": customers, "success": False, "error_message": errors_list}

        else:
            update_customer_result = {"customers": update_customer_result["customers"], "success": True, "error_message": errors_list}


    return update_customer_result


def is_deposit_valid(param_deposit_value) -> bool:
    """
    Check if the deposit transaction amount is greater than 0 (zero).

    Args:
        param_deposit_value (int): Value of the deposit transaction.

    Returns:
        bool: If the deposit transaction value is greater than 0 (zero), True will be returned.
    """ 

    return param_deposit_value > 0


def build_bank_statement(param_withdraw_money, param_account_balance, param_currency_identifier)-> str:
    """
    Generates text describing the customer's banking transactions.

    Args:
        param_withdraw_money (str): Description of the customer's withdrawal transaction.
        param_account_balance (float): Current balance of the customer's account.
        param_currency_identifier (str): A monetary identifier to link to the customer's bank transaction records.

    Returns:
        str: Returns text describing the customer's banking transactions.
    """ 

    TOP_BORDER_CHARACTER = "="
    ROW_LENGTH_DEFAULT = 80
    HEADER_TITLE = " Withdraw Money "
    BOTTOM_BORDER_CHARACTER = "="
    EMPTY_STRING = ""
    MESSAGE_DEFAULT_TO_NO_TRANSACTION = "No transactions were carried out."

    top_border = HEADER_TITLE.center(ROW_LENGTH_DEFAULT, TOP_BORDER_CHARACTER)
    bottom_border = EMPTY_STRING.center(ROW_LENGTH_DEFAULT, BOTTOM_BORDER_CHARACTER)
    records_already_made = f"{"No transactions were carried out." if not param_withdraw_money else param_withdraw_money}"
    current_record = f"Account balance: {param_currency_identifier} {param_account_balance:.2f}"

    content = f"{top_border}"
    content += f"\n{records_already_made}"
    content += f"\n{current_record}"
    content += f"\n{bottom_border}"

    return content


def make_address() -> Result_Create_Address:
    print("\nPlease provide the new customer's address: ")

    value_input_street          = input("Street/Avenue/Road: ")     # "Street_#1"       
    value_input_number          = input("Number: ")                 # "123D"            
    value_input_neighborhood    = input("Neighborhood: ")           # "Neighborhood#1"  
    value_input_city            = input("City: ")                   # "City#1"          
    value_input_state           = input("State: ")                  # "State#1"         

    result = build_address(value_input_street, value_input_number, value_input_neighborhood, value_input_city, value_input_state)

    return result 


def build_address(param_street, param_number, param_neighborhood, param_city, param_state) -> Result_Create_Address:
    
    new_Address = {
         "street": param_street
        ,"number": param_number
        ,"neighborhood":  param_neighborhood
        ,"city": param_city
        ,"state": param_state
    }

    create_result = {
         "address":new_Address
        ,"success": True
        ,"error_messages":[]
    }

    return create_result


def make_customer(param_customers: Customers) -> Result_Make_Customer:

    customers = param_customers.copy()

    print("Please provide the new customer's details: ")

    value_input_name                     = input("name               : ")                           
    value_input_birth_date               = input("Expected format: yyyy-mm-dd\nbirth_date    : ")   
    value_input_cpf                      = input("cpf                : ")                           
    
    cpf_sinitized = sanitize_cpf(value_input_cpf, True)
    customer_exists, customer = customer_already_exist(cpf_sinitized, customers)

    if customer_exists:
        error_list = ["Customer's cpf already exists."]
        result = dict(customers = customers, customer = None, success = False, error_messages = error_list) 
        return result

    value_input_account_balance          = input("account_balance    : ") 
    
    value_input_value_limit_withdrawalas = input("value_limit_withdrawalas  : ") 
    if value_input_value_limit_withdrawalas.isdigit():
        value_input_value_limit_withdrawalas = int(value_input_value_limit_withdrawalas)

    else:
        value_input_value_limit_withdrawalas = 0


    value_input_limit_withdrawals        = input("limit_withdrawals  : ") 
    if value_input_limit_withdrawals.isdigit():
        value_input_limit_withdrawals = int(value_input_limit_withdrawals)

    else:
        value_input_limit_withdrawals = 0

    value_input_address                  = make_address()

    if not value_input_address or not value_input_address["success"]:
        result = dict(customers = customers, customer = None, success = value_input_address["success"], error_messages = value_input_address["error_messages"]) 
        return result

    else:
        new_customer = build_customer(   value_input_name                
                                        ,value_input_birth_date          
                                        ,value_input_cpf                 
                                        ,value_input_address["address"] 
                                        ,value_input_account_balance     
                                        ,value_input_limit_withdrawals   
                                        ,value_input_value_limit_withdrawalas
                                    )

    register = register_customer(new_customer["customer"], customers)

    if not register["success"]:
        result = dict(customers = register["customers"], customer = None, success = register["success"], error_messages = register["error_messages"]) 

    else:
        result = dict(customers = register["customers"], customer = new_customer["customer"], success = register["success"], error_messages = []) 

    return result


def build_customer(param_name, param_birth_date, param_cpf, param_address:Address, param_account_balance, param_limit_withdrawals = WITHDRAW_LIMIT, param_value_limit_to_waldrawalas=VALUE_LIMIT_WALDRAWALAS) -> Result_Create_Customer:

    DEFAULT_VALUE_TO_WITHDRAW_MONEY = ""
    DEFAULT_VALUE_FOR_NUMBER_OF_WITHDRAWALS = 0

    new_customer = {
        "name": param_name,
        "birth_date": param_birth_date,
        "cpf": sanitize_cpf(param_cpf, True),
        "address": param_address, 
        "account_balance": float(param_account_balance),
        "withdraw_money": DEFAULT_VALUE_TO_WITHDRAW_MONEY,
        "amount_of_withdraws": DEFAULT_VALUE_FOR_NUMBER_OF_WITHDRAWALS,
        "limit_withdrawals": param_limit_withdrawals if is_valid_limit_of_withdraw(param_limit_withdrawals) else WITHDRAW_LIMIT,
        "value_limit_waldrawalas": param_value_limit_to_waldrawalas if is_valid_value_to_withdrawalas(param_value_limit_to_waldrawalas) else VALUE_LIMIT_WALDRAWALAS
    }

    create_result = {
         "customer":new_customer
        ,"success": True
        ,"errors_message":[]
    }

    return create_result


def is_valid_limit_of_withdraw(param_limit_of_withdraw:int) -> bool:
    return param_limit_of_withdraw > 0


def is_valid_value_to_withdrawalas(param_value_to_withdrawalas:int) -> bool:
    return param_value_to_withdrawalas > 0


def sanitize_cpf(param_cpf:str, param_remove_blank_spaces_right_left: bool) -> str:
    dict_characters_to_sanitized_cpf = dict([("-", "" ), (".", "" )])

    return remove_filtered_characters(param_cpf, param_remove_blank_spaces_right_left, characters_to_replace = dict_characters_to_sanitized_cpf)


def remove_filtered_characters (param_value:str, param_remove_blank_spaces_right_left: bool, characters_to_replace: Characters_To_Replace) -> str:
    
    if not characters_to_replace:
        return param_value

    if not param_value:
        return param_value

    sanitized_value = param_value

    for character_searched, character_substitute in characters_to_replace.items():
        if character_searched in sanitized_value:
            sanitized_value = sanitized_value.replace(character_searched, character_substitute)

    if param_remove_blank_spaces_right_left:
        sanitized_value.strip()

    return sanitized_value


def register_customer(param_customer: Customer, param_customers: Customers) -> Result_Register_Customer:
    customer_exists, customer = customer_already_exist(param_customer["cpf"], param_customers)
    if customer_exists:
        return { "customers": param_customers, "success": False, "error_messages": ["Customer already exist. It is not possible to register them again."]}

    updated_customers = param_customers.copy() 
    updated_customers.append(param_customer)

    return { "customers": updated_customers, "success": True, "error_messages": []}


def update_customer(param_customer: Customer, param_customers: Customers) -> Result_Update_Customer:
    customer_exists = customer_already_exist(param_customer["cpf"], param_customers)

    if not customer_exists:
        return { "customers": param_customers, "success": False, "error_messages": ["Customer not exists. It is not possible to update them."]}

    updated_customers = param_customers.copy() 
    for index, customer in enumerate(updated_customers):
        if customer["cpf"] == param_customer["cpf"]:
            updated_customers[index] = param_customer
            break

    return { "customers": updated_customers, "success": True, "error_messages": []}


def customer_already_exist(param_cpf: str, param_customers: Customers) -> (bool, Customer):
    
    if len(param_customers) == 0:
        return False, None
    
    dict_Customers = {item["cpf"]: item for item in param_customers}
    exists = param_cpf in dict_Customers.keys()
    customer = dict_Customers.get(param_cpf, None)

    return exists, customer


def make_search_by_customer(customers: Customers) -> Result_Search_Customer:
    print("Search By Customer")
    customers_cpf_searched = input("Type customer's cpf: ")

    return get_customer(customers_cpf_searched, customers)


def get_customer(client_cpf:str, customers: Customers) -> Result_Search_Customer:
    client_cpf_sanitized = sanitize_cpf(client_cpf, True)

    exist, customer_finded = customer_already_exist(client_cpf_sanitized, customers)

    if not exist:
        return { "customer": None, "success": exist, "error_messages": ["Customer not finded."]  }    

    return { "customer": customer_finded, "success": exist, "error_messages": []  }


## Main rotine
while True:

    option = input(MENU)

    if option == "c":
        result = make_customer(customers_bank)

        if result["success"]:
            customers_bank = result["customers"]
            print(f"Success!!\n Clients updated: {customers_bank}")

        else:
            print(f"Something unexpected occured.\nErrors: {result["error_messages"]}")

    
    elif option == "d":
        customer_search_result = make_search_by_customer(customers_bank)

        if not customer_search_result["success"]:
            error_message = customer_search_result["error_messages"] 
            print(error_message,sep="\n")
            continue

        customer = customer_search_result["customer"].copy()

        deposit_result = make_deposit(customer, customers_bank)

        if not deposit_result or not deposit_result["success"]:
            print(deposit_result["error_message"])
        else:
            customers_bank = deposit_result["customers"]


    elif option == "w":
        customer_search_result = make_search_by_customer(customers_bank)

        if not customer_search_result["success"]:
            error_message = customer_search_result["error_messages"] 
            print(error_message,sep="\n")
            continue

        customer = customer_search_result["customer"].copy()

        withdraw_result = make_withdraw(param_customer=customer, param_customers=customers_bank)
        
        if not withdraw_result["success"]: 
            error_message = withdraw_result["error_messages"] 
            print(error_message,sep="\n")
            continue

        else: 
            customers_bank = withdraw_result["customers"]


    elif option == "s":
        customer_search_result = make_search_by_customer(customers_bank)

        if not customer_search_result["success"]:
            error_message = customer_search_result["error_messages"] 
            print(error_message,sep="\n")
            continue

        customer = customer_search_result["customer"].copy()

        bank_statement = build_bank_statement(customer["withdraw_money"], param_currency_identifier= CURRENCY_IDENTIFIER, param_account_balance=customer["account_balance"])
        print(bank_statement)

    elif option == "e":
        break

    else:
        print("Invalid operation, please select the desired operation again.")
