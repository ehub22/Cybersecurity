# old_pass = input("Enter passord: ")
# new_pass = []
# pass_list = list(old_pass)
# for i in range(len(pass_list)):
#     letter = ord(old_pass[i])+3
#     print(ord(old_pass[i]))
#     print(letter)
#     new_pass.append(chr(letter))
#     print(new_pass)

def encrypt():
    old_pass = input("Enter password: ")
    new_pass_list = []
    old_pass_list = list(old_pass)
    new_pass = ""
    for i in range(len(old_pass_list)):
        letter = ord(old_pass[i]) + 3
        print(ord(old_pass[i]))
        print(letter)
        new_pass_list.append(chr(letter))
        print(new_pass_list)
    new_pass = "".join(map(str,new_pass_list))
    return(new_pass)

# print(encrypt())