cpu_hrs=int(input("enter number of cpu hrs:"))
storage=int(input("enter storage in gb:"))
transfer=int(input("enter transfer in gb:"))
cpu_cost=cpu_hrs*5
storage_cost=storage*2
transfer_cost=transfer*1
total_amount=cpu_cost+storage_cost+transfer_cost
if cpu_hrs>100:
    print(total_amount+500)
else:
    print(total_amount)