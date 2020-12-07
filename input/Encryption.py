import os
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import pss
import ast

def generate_rsa_keys(modulus,private_file,public_file,mod_exp = 65537):
    """
    Function that generates a pair of RSA Keys, and returns either the private or public key depending on the argument

    modulus -> RSA modulus length

    private_file & public file -> names for the files of the generated keys

    mod_exp -> public exponent value. if left blank it defaults to 65537
    """
    key = RSA.generate(modulus, e=mod_exp)
    private_key = key.exportKey("PEM")
    public_key = key.publickey().exportKey("PEM")
    with open(private_file,'wb') as file:
        file.write(private_key)
    with open(public_file,'wb') as file:
        file.write(public_key)

def iv_key():
    iv = binascii.hexlify(os.urandom(8)) # random IV with 8 bytes
    aes_key = binascii.hexlify(os.urandom(16))
    with open("aes_key.key",'wb') as file:
        file.write(aes_key)
        file.write(iv)
    print("AES Key Created")

def read_iv_key():
    with open("aes_key.key",'rb') as file:
        aes_key = file.read()
    return(aes_key)

def rsa_encryption(data, type, user = ''):
    """
    data -> data that needs to be encrypted
    type -> str: user or server
    user -> for user private/public key. Used for signatures
    """
    if type == 'server':
        encoded_data = data.encode()
        hex_data = binascii.hexlify(encoded_data)
        server_public_key = RSA.importKey(open("server_public.pem").read())
        cipher = PKCS1_OAEP.new(server_public_key)
        secure = cipher.encrypt(hex_data)
        return secure
    elif type == 'user':
        encoded_data = data.encode()
        hex_data = binascii.hexlify(encoded_data)
        user_public_key = RSA.importKey(open("user_public.pem").read())
        cipher = PKCS1_OAEP.new(user_public_key)
        secure = cipher.encrypt(hex_data)
        return secure
    else:
        return "Invalid Type"

def rsa_decryption(data, type, user=''):
    """
    data -> data that needs to be decrypted
    type -> str: user or server
    """
    if type == 'server':
        server_private_key = RSA.importKey(open("server_private.pem").read())
        plain = PKCS1_OAEP.new(server_private_key)
        decrypt = plain.decrypt(data)
        un_hex = binascii.unhexlify(decrypt)
        un_dec = un_hex.decode()

        return un_dec

    elif type == 'user':
        user_private_key = RSA.importKey(open("user_private.pem").read())
        plaintext = PKCS1_OAEP.new(user_private_key)
        decrypt = plaintext.decrypt(data)
        un_hex = binascii.unhexlify(decrypt)
        un_dec = un_hex.decode()

        return un_dec

    else:
        return "Invalid Type"

def signature(sig,private_key):
    """
    Function that creates an e-signature using SHA256 and private keys
    sig -> data that will be used as the signature
    user -> the user, in order to use their private key
    returns a list with the signature, and hash-value
    """
    sig = sig.encode()
    user_private_key = RSA.importKey(open(private_key).read())
    hash_value = SHA256.new(sig)
    e_signature = pss.new(user_private_key).sign(hash_value)
    return e_signature

def sig_verifier(sig, public_key,hash_value):
    """
    Function that verifies the e-signature using SHA256 and public keys
    sig -> te signature that needs to be verified
    public_key -> the users public key
    hash_value -> the hash value that is return from the signature
    returns: True if it passes verification
             False if it doesnt pass verification
    """
    user_public_key = RSA.importKey(open(public_key).read())
    verifier = pss.new(user_public_key)
    try:
        verifier.verify(hash_value,sig)
        return True
    except:
        return False
