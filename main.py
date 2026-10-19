while True:
    user_input = input("Enter the first number (or type q to quit): ")

    if user_input.lower() == 'q':
        break

    number1 = float(user_input)
    operator = input("Enter an operator (+, -, *, /): ")
    num2 = float(input("Enter the second number: "))

    if operator == '+':
        result = number1 + num2
    elif operator == '-':
        result = number1 - num2
    elif operator == '*':
        result = number1 * num2
    elif operator == '/':
        if num2 == 0:
            print("You can't divide by zero!")
            continue
        result = number1 / num2
    else:
        print("Invalid operator")
        continue

    print("The answer is:", result)
