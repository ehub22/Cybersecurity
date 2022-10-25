def generate_key(string, key):
    key = list(key)



    if len(string) == len(key):
        return key


    else:
        for i in range(len(string)-len(key)):

            key.append(key[i % len(key)])
            print(key)

    # return "".join(key)

# def cipher_text(string, key):
#     cipher_text = []

generate_key("Hello", "Hi")
