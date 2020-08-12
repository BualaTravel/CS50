import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: Invalid input.")
    sys.exit(1)

try:
    result = x / y
except ZeroDivisionError:
    print("Error: Cannot be divided by 0.")
    sys.exit(1) #status called of 1 means something went wrong in the program

print(f"{x} / {y} = {result}")
