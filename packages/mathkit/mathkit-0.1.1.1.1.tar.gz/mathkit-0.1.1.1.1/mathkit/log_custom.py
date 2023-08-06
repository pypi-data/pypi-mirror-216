def log():
    print("Logarithm")
    print("1. Logarithm of 2")
    print("2. Logarithm of 10")
    print("3. Logarithm of any number")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        import math
        print(math.log(2))
    elif choice == 2:
        import math
        print(math.log(10))
    elif choice == 3:
        import math
        num = int(input("Enter the number: "))
        print(math.log(num))
    elif choice == 4:
        exit()
    else:
        print("Invalid choice!")
        log()