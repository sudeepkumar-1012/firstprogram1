correct_password = "admin123"
for attempt in range(1,4):
    password = input("enter your password: ")
    if password == correct_password:
        print("login sucessfull")
        break
    else:
        print("wrong password")

        if attempt == 3:
            print("Account locked")