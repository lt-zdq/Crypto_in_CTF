from Crypto.Cipher import AES
import os

# 加密端
# flag = open("flag").read()
flag = 'hellochenMsgH888888H'   
key = os.urandom(16)
aes = AES.new(key, AES.MODE_ECB)


# while True:
def encry(userName):
    # name = input("Your name: ")
    name = userName
    msg = "Hello, " + name + "! Your flag is " + flag
    msg = msg.encode()
    msg += b"\x00" * (-len(msg) % AES.block_size)
    enc = '' + aes.encrypt(msg).hex()
    return enc


#userName = '**'
#print(encry())


# 解题端
lenStr = len("Hello, ") + len("! Your flag is ")

def getFlagLen():
    name = ''
    lenOri = len(bytes.fromhex(encry(name)))
    # print(lenOri)

    while True:
        name += 'a'
        length = len(bytes.fromhex(encry(name)))
        if length != lenOri:
            lenPadding = len(name) - 1
            lenFlag = lenOri - lenStr - lenPadding
            return lenFlag
            break

# print(getFlagLen())


def forceFlag(length):
    lenPadding = -(lenStr + length)%16
    flag = ''
    flagStartInedx = 2*(lenStr + length + lenPadding)
    
    # print(flagStartInedx)

    for i in range(length):
        # 增加padding长度，flag被挤出来，每次挤出一位，flag长度大于AES.block_size时，只管新挤出来的block，旧的在后面的block
        padStr = 'a'*(lenPadding + i + 1)
        enc = encry(padStr)
        flagEnc = enc[flagStartInedx: flagStartInedx+2*AES.block_size]
        
        # 爆破flag，爆破的内容放到"Hello, "之后，先把"Hello, "补齐，然后开始爆破位
        pad1 = '*'*(-len("Hello, ")%16)
        for ch in range(0x00, 0x7f):
            forceStr = pad1 + chr(ch) + flag + '\x00'*(-(len(flag)+1)%16)
            enc = encry(forceStr)
            
            forceEnc = enc[2*AES.block_size: 4*AES.block_size]
            if forceEnc == flagEnc:
                flag = chr(ch) + flag
                # print(flag)
                break

    return flag


print(forceFlag(getFlagLen()))
