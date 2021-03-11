from Crypto.Cipher import AES
import os

flag = open("flag").read()
key = os.urandom(16)
aes = AES.new(key, AES.MODE_ECB)
while True:
    name = input("Your name: ")
    msg = "Hello, " + name + "! Your flag is " + flag
    msg = msg.encode()
    msg += b"\x00" * (-len(msg) % AES.block_size)
    print(aes.encrypt(msg).hex())
