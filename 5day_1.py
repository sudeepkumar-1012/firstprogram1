unit=int(input("enter the unit:"))
if unit <= 100:
    bill=unit*1
elif unit <= 200:
    bill=unit*1 + (unit-100)*2
else:
    bill=unit*1+unit*2+(unit-200)*5
print("electricity bill:",bill)