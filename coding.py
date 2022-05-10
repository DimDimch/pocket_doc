import rsa
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

# privateKey = 0
# publicKey = 0


"""
в кратце смысл шифрования: мы берём публичный ключ чела и шифруем сообщение, 
разшифровать его можно только с помощью приватного ключа
пример использования 
import coding

message="hello"
code=coding.encrypt(message)
print(code)
message=coding.dencrypt(code)
print(message)
"""

key = RSA.generate(2048)
privateKey = key.exportKey('PEM')
publicKey = key.publickey().exportKey('PEM')


def encrypt(message, key):
    message = str.encode(message)
    RSApublicKey = RSA.importKey(key)
    OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
    encryptedMsg = OAEP_cipher.encrypt(message)

    # print('Encrypted text:', encryptedMsg)
    return encryptedMsg

    # RSAprivateKey = RSA.importKey(privateKey)


def dencrypt(code):
    RSAprivateKey = RSA.importKey(privateKey)
    OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
    decryptedMsg = OAEP_cipher.decrypt(code)
    # print('The original text:', decryptedMsg)
    return decryptedMsg

