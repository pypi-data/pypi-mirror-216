def percent():
    print("1. Percentage of a number")
    print("2. Percentage increase")
    print("3. Percentage decrease")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        num = float(input("Enter the number: "))
        per = float(input("Enter the percentage: "))
        print(str(per) + "% of " + str(num) + " is " + str((per/100)*num))
    elif choice == 2:
        num = float(input("Enter the number: "))
        per = float(input("Enter the percentage: "))
        print(str(num) + " increased by " + str(per) + "% is " + str(num + ((per/100)*num)))
    elif choice == 3:
        num = float(input("Enter the number: "))
        per = float(input("Enter the percentage: "))
        print(str(num) + " decreased by " + str(per) + "% is " + str(num - ((per/100)*num)))
    elif choice == 4:
        exit()
    else:
        print("Invalid choice!")
        per()