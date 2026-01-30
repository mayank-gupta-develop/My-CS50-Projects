# Get credit card number
number = input("Number: ")

# Check if input is numeric
if not number.isdigit():
    print("INVALID")
    exit()

length = len(number)

# Luhn's Algorithm
total = 0
reverse_digits = number[::-1]

for i in range(length):
    digit = int(reverse_digits[i])

    if i % 2 == 1:
        digit *= 2
        if digit > 9:
            digit -= 9

    total += digit

# Check validity
if total % 10 != 0:
    print("INVALID")
    exit()

# Check card type
if length == 15 and number.startswith(("34", "37")):
    print("AMEX")
elif length == 16 and number.startswith(("51", "52", "53", "54", "55")):
    print("MASTERCARD")
elif length in [13, 16] and number.startswith("4"):
    print("VISA")
else:
    print("INVALID")
