import hashlib
from itertools import product
import time
from Cesar_Encrypter import *

#5ebe2294ecd0e0f08eab7690d2a6ee69
alphabet = "abcdefghiklmnoprstuvwy!"

#word = imput
#encoded = word.encode()
#hashed = hashlib.md5(encoded).hexdigest()

hashed = input("What is your password? ")
print(hashed)
hashed = hashed.encode()
hashed = hashlib.md5(hashed).hexdigest()
minLength = int(input("Minimum Password Length:"))
maxLength = int(input("Maximum Password Length:"))
password = ""

for i in range(minLength, maxLength + 1):
    for possibility in product(alphabet, repeat=i):
        #print(possibility)
        possibility = "".join(possibility)
        encodedPossibility = possibility.encode()
        tester = hashlib.md5(encodedPossibility).hexdigest()
        #print(possibility + " -> " + tester)
        if tester == hashed:
            print("Password found: " + possibility)
            password = possibility
            break

if password == "":
    print("Error. No password found.")

def cracker():
    for i in range(minLength, maxLength + 1):
        for possibility in product(alphabet, repeat=i):
            # print(possibility)
            possibility = "".join(possibility)
            encodedPossibility = possibility.encode()
            tester = hashlib.md5(encodedPossibility).hexdigest()
            # print(possibility + " -> " + tester)
            if tester == hashed:
                print("Password found: " + possibility)
                password = possibility
                break