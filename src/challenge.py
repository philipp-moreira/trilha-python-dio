MENU = """

[d] Deposit
[w] Withdraw money
[s] Bank statement
[e] Exit

=> """

CURRENCY_IDENTIFIER = "R$"
WITHDRAW_LIMIT = 3

account_balance = 0
limit_withdrawals = 500
withdraw_money = ""
amount_of_withdraws = 0

while True:

    option = input(MENU)

    if option == "d":
        value = float(input("Please provide the deposit amount: "))

        if value > 0:
            account_balance += value
            withdraw_money += f"Deposit: {CURRENCY_IDENTIFIER} {value:.2f}\n"

        else:
            print("The operation failed! The value entered is invalid.")

    elif option == "w":
        value = float(input("Please provide the withdrawal amount: "))

        exceeded_account_balance = value > account_balance

        exceeded_limit = value > limit_withdrawals

        exceeded_withdrawals = amount_of_withdraws >= WITHDRAW_LIMIT

        if exceeded_account_balance:
            print("Operation failed! You do not have sufficient account balance.")

        elif exceeded_limit:
            print("The transaction failed! The withdrawal amount exceeds the limit.")

        elif exceeded_withdrawals:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        elif value > 0:
            account_balance -= value
            withdraw_money += f"Withdraw money: {CURRENCY_IDENTIFIER} {value:.2f}\n"
            amount_of_withdraws += 1

        else:
            print("The operation failed! The value entered is invalid.")

    elif option == "s":
        print("\n================ withdraw_money ================")
        print("No transactions were carried out." if not withdraw_money else withdraw_money)
        print(f"\nAccount balance: {CURRENCY_IDENTIFIER} {account_balance:.2f}")
        print("==========================================")

    elif option == "e":
        break

    else:
        print("Invalid operation, please select the desired operation again.")
