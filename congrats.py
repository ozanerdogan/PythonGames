import time
import os

def clear():
    os.system( 'cls' )

def congrats():
    print((" | " * x + "\n") * (x//2) + "   CONGRATS!!\n" + (" | " * x + "\n") * (x//2))

x = 10

for i in range(x//2):
    print("   " * i + " * " + "   " * (x - 2*i - 2) + " * ")
    print("\n" * (x- 2*i -2))
    print("   " * i + " * " + "   " * (x - 2*i - 2) + " * ")
    time.sleep(0.3)
    clear()

if x % 2 == 1:
    print("\n" * (x//2) + "   " * (x//2) + " * ")
    time.sleep(1)
    clear()

congrats()
clear()
time.sleep(0.3)
congrats()
clear()
time.sleep(0.3)
congrats()
clear()
time.sleep(0.3)
congrats()
clear()
time.sleep(0.3)
congrats()
clear()
time.sleep(0.3)
congrats()
time.sleep(3)


