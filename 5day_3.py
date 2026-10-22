age=int(input("enter the age:"))
if age>=18:
    print("allowed for match")
    if age >= 18 and age < 30:
        print("2$ ticket price")
    elif age >= 30 and age < 60:
        print("1$ ticket price")
    else:
        print("0$ ticket price")
else:
    print("not allowed for match")