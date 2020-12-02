##################################################################################
#### THIS IS JUST FOR ME TO TEST STUFF NOT FOR THE FINAL ITERATION OF PROJECT ####
##################################################################################
import binascii
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import pss


# dummy variables for testing
#dummy_ssn = input("Enter your SSN: ")
#dummy_birth = input("Enter your birthdate (dd/mm/yyyy): ")
dummy_vote = str(input("Enter your preferred Candidate: "))


#dummy_ssn = dummy_ssn.encode()
#dummy_birth = dummy_birth.encode()
dummy_vote = dummy_vote.encode()

#ssn_sec = binascii.hexlify(dummy_ssn)
#birth_sec = binascii.hexlify(dummy_birth)
vote_sec = binascii.hexlify(dummy_vote)
print(vote_sec)
# ssn_return = binascii.unhexlify(ssn_sec)
# vote_return = binascii.unhexlify(vote_sec)


# RSA implementations

#  TODO: FIND A BETTER WAY TO GENERATE KEYS
#   THIS GENERATION METHOD IS A BIT BULKY AND CAN BE IMPROVED
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

iv_key()
aes_key_iv = read_iv_key()
aes_key = aes_key_iv[:32]
aes_iv = aes_key_iv[32:]




user_keys = generate_rsa_keys(1024, 'user_private.pem','user_public.pem')
server_keys = generate_rsa_keys(1024,'server_private.pem','server_public.pem')

server_public_key = RSA.importKey(open('server_public.pem').read())
server_private_key = RSA.importKey(open('server_private.pem').read())

user_public_key = RSA.importKey(open('user_public.pem').read())
user_private_key = RSA.importKey(open('user_private.pem').read())

vote_cipher = PKCS1_OAEP.new(user_public_key)
sec_vote = vote_cipher.encrypt(vote_sec) # encrypt using user private key
print(sec_vote)

# Encrypt using AES
aes_cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv) # CBC Mode AES - for encryption
ciphered_data = aes_cipher.encrypt(pad(sec_vote, AES.block_size))
print(ciphered_data)

#Decrypt AES
aes_plain = AES.new(aes_key, AES.MODE_CBC, aes_iv) # CBC Mode AES - for decryption
original_sec_vote = unpad(aes_plain.decrypt(ciphered_data), AES.block_size)
print(original_sec_vote)

# Decrypt RSA using RSA private key
vote_plaintext = PKCS1_OAEP.new(user_private_key)
decrypt_vote = vote_plaintext.decrypt(original_sec_vote)
print(decrypt_vote)

vote_return = binascii.unhexlify(decrypt_vote)
print(vote_return.decode())

# Candidate name - here so i can just copy paste to console : Marcus Maragh

# Decrypt RSA
#vote_decrypt = PKCS1_OAEP.new(user_public_key)
#what = vote_decrypt.decrypt(plaintext)
#print(what)
## signature
# h = SHA256.new(ssn_sec)
# signature = pss.new(user_private_key).sign(h)
#
# verifier = pss.new(user_public_key)
# try:
#     verifier.verify(h,signature)
#     print("Signature is Authentic")
# except (ValueError,TypeError):
#     print("The signature is not authentic")


