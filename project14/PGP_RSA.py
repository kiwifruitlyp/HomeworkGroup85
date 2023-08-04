#!usr/bin/python
# encoding:utf-8
import base64
import hashlib
import re
import os
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import time
def writefile(data, filepath):
    if type(data) == bytes:
        msg = str(data, encoding='utf-8')
    elif data.inStanceOf(str):
        msg = data
    else:
        print("该数据格式不支持文件写入")
        return False
 
    f = open(filepath, 'w')
    f.write(msg)
    f.close()
    return True
 
 
def readfile(filepath):
    f = open(filepath, 'r')
    data = f.read()
    f.close()
    return data
 
 
#使用口令与盐，创建对称密钥与初始化向量
def get_derived_key(password, salt, count):
    key = str(password)+ str(salt)
    for i in range(count):
        m = hashlib.md5(str(key).encode('utf-8'))
        key = m.digest()
    return (key[:8], key[8:])
 
# DES-CBC解密
def decrypt(msg, password):
    msg_bytes = base64.b64decode(msg)
    salt = msg_bytes[:8]
    enc_text = msg_bytes[8:]
    (dk, iv) = get_derived_key(password, salt, 1000)
 
    crypter = DES.new(dk, DES.MODE_CBC, iv)
    text = crypter.decrypt(enc_text)
    # remove the padding at the end, if any
    return re.split(b'[\x01-\x08]',text)[0]
   #return re.sub(r'[\x01-\x08]', '', text.decode())
 
 
 
# DES-CBC 加密
def encrypt(msg, password):
    salt = os.urandom(8)
    data = msg.encode(encoding='utf-8')
    pad_num = 8 - (len(data) % 8)
    for i in range(pad_num):
        data += chr(pad_num).encode(encoding='utf-8')
    (dk, iv) = get_derived_key(password, salt, 1000)
 
    crypter = DES.new(dk, DES.MODE_CBC, iv)
    enc_text = crypter.encrypt(data)
    return base64.b64encode(salt + enc_text)
 
 
# 用于解密对称会话密钥
class RSA_encryto:
    def __init__(self):
        rsa = RSA.generate(1024, Random.new().read)
        private = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
        self.__private_key = private
        self.public_key = public_key
        self.__rsa = rsa
 
    def export_public_key(self):
        return self.public_key
 
 
    def export_encypted_private_key(self):
        salt = os.urandom(8)
 
        private = self.__private_key
 
        pad_num = 8 - (len(private) % 8)
        for i in range(pad_num):
            private += chr(pad_num).encode(encoding='utf-8')
        password = input("口令:")
        (dk, iv) = get_derived_key(password, salt, 1000)
 
        crypter = DES.new(dk, DES.MODE_CBC, iv)
        enc_text = crypter.encrypt(private)
        return base64.b64encode(salt + enc_text)
 
 
 
def main():
    rsa = RSA_encryto()     #创建rsa实体对象
    commuicate_key = "helloworld"     #产生会话密钥
    msg = input("msg:")         #读取msg
    ec_msg = encrypt(msg, commuicate_key)    #加密消息msg
 
    # 1. 导出rsa密钥到pc上
    ec_private_key_path = input('请输入密钥保存位置：(默认为./ec_private_key)')
    if ec_private_key_path == '':
        ec_private_key_path = './ec_private_key'
    ec_private_key = rsa.export_encypted_private_key()
    print ("加密后rsa密钥:"+str(ec_private_key))
    writefile(ec_private_key, ec_private_key_path)
    print("加密后rsa密钥保存在：" + ec_private_key_path)
 
    # 2. RSA加密会话密钥
    publickey = rsa.export_public_key()
    rsakey = RSA.importKey(publickey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(commuicate_key.encode(encoding='utf-8')))
#    cipher_text = cipher.encrypt(commuicate_key)
    ec_msg_path = input('请输入加密文件保存位置：(默认为./ec_msg)')
    if ec_msg_path == '':
        ec_msg_path = './ec_msg'
    ec_commuicate_key_path = input('请输入加密密钥保存位置：(默认为./ec_commuicate_key_path)')
    if ec_commuicate_key_path == '':
        ec_commuicate_key_path = './ec_commuicate_key_path'
    print("加密文件内容：" + str(ec_msg)+ ", 加密会话密钥为: "+str(cipher_text))
    writefile(ec_msg, ec_msg_path)
    writefile(cipher_text, ec_commuicate_key_path)
    print("加密文件保存在："+ ec_msg_path +", 加密会话保存在: " + ec_commuicate_key_path)
 
# 从文件中导入加密私钥
    ec_private_key_path = input('请输入密钥保存位置：(默认为./ec_private_key)')
    if ec_private_key_path == '':
        ec_private_key_path = './ec_private_key'
    de_private_key = readfile(ec_private_key_path)
 
 
    while(True):
        # 3. 解密RSA私钥
        password = input("口令:")
        rsa_privatekey = decrypt(de_private_key, password)
 
        # 4. 解密会话密钥
        try:
            global rsa_key
            rsa_key = RSA.importKey(rsa_privatekey)  # 导入读取到的私钥
            break
        except ValueError:
            print ("口令错误")
 
    ec_msg_path = input('请输入加密文件保存位置：(默认为./ec_msg)')
    if ec_msg_path == '':
        ec_msg_path = './ec_msg'
    ec_commuicate_key_path = input('请输入加密密钥保存位置：(默认为./ec_commuicate_key_path)')
    if ec_commuicate_key_path == '':
        ec_commuicate_key_path = './ec_commuicate_key_path'
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)  # 生成对象
    commuicatekey = cipher.decrypt(base64.b64decode(readfile(ec_commuicate_key_path)), "ERROR")
#    commuicatekey = cipher.decrypt(cipher_text, "ERROR")
 
    # 5. 解密msg
    de_msg = decrypt(readfile(ec_msg_path), str(commuicatekey, encoding='utf-8'))
    print("msg:" + str(de_msg, encoding='utf-8'))
 
start_time = time.perf_counter()
if __name__ == "__main__":
    main()
end_time = time.perf_counter()
print('程序运行时间:', end_time - start_time, '秒')
