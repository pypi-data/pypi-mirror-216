from setuptools import setup

setup(
    name='mathkit',
    version='0.1.1',
    description='Math Simplifies - A Python library for mathematical calculations.',
    long_description='''Math Simplifies is a Python library that provides various mathematical functions and utilities for performing common mathematical calculations.

Example Usage:
from addition import add
from subtract import sub
from multiply import mul
from division import div
from modulas import mod
from power import power
from square import sqr
from cube import cube
from square_root import sqrt
from cube_root import cbrt
from factorial import fact
from percentage import percent
from remainder import remain
from lcm_custom import lcm
from hcf_custom import hcf
from log_custom import log

print("Welcome to the Math Library!")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("5. Modulas")
print("6. Power")
print("7. Square")
print("8. Cube")
print("9. Square Root")
print("10. Cube Root")
print("11. Factorial")
print("12. Percentage")
print("13. Remainder")
print("14. LCM")
print("15. HCF")
print("16. Logarithm")
print("17. Exit")

choice = int(input("Enter your choice: "))

if choice == 1:
    add()
elif choice == 2:
    sub()
elif choice == 3:
    mul()
elif choice == 4:
    div()
elif choice == 5:
    mod()
elif choice == 6:
    power()
elif choice == 7:
    sqr()
elif choice == 8:
    cube()
elif choice == 9:
    sqrt()
elif choice == 10:
    cbrt()
elif choice == 11:
    fact()
elif choice == 12:
    percent()
elif choice == 13:
    remain()
elif choice == 14:
    lcm()
elif choice == 15:
    hcf()
elif choice == 16:
    log()
elif choice == 17:
    exit()
else:
    print("Invalid choice!")
    print("Press Enter to continue")
    input()
''',
    author='TheUnkownHacker',
    author_email='theunkownhecker@gmail.com',
    url='https://github.com/theunkownhacker/mathkit',
    packages=['mathkit'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
