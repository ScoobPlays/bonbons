first_input = int(input("First: "))
second_input = int(input("Second: "))
operation_question = input("Operation: ")

if operation_question == "+":
    print(first_input + second_input)
    return

if operation_question == "-":
    print(first_input - second_input)
    return

if operation_question == "*":
    print(first_input * second_input)
    return

if operation_question == "/":
    print(first_input / second_input)
    return

if operation_question == "//":
    print(first_input // second_input)
    return
