##################################################################################
#### THIS IS JUST FOR ME TO TEST STUFF NOT FOR THE FINAL ITERATION OF PROJECT ####
##################################################################################
import json
import binascii
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from Crypto.Signature import pss


with open("user.json") as file:
    vote_data = json.load(file)

votes_list = []
for i in range(len(vote_data)):
    vote = str(i)
    ind_vote = vote_data[vote]['Votes']
    vote_l= list(ind_vote.values())
    votes_list.append(vote_l)
print(votes_list)


def string_list(x):
    """
    x: -> a list
    return: the same list, but the values will be a string
    """
    str_lst = list(map(str, x))
    return str_lst

dummy_vote = []
for i in range(len(vote_data)):
    lst_str = string_list(votes_list[i])
    dummy_vote.append(lst_str)

print(dummy_vote)

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


## Generate User Keys
private_name_start = "user_private"
public_name_start = "user_public"
private_list = []
public_list = []
for i in range(len(vote_data)):
    user_id = str(i)
    private_name = private_name_start + '_' + user_id + '.pem'
    private_list.append(private_name)
    public_name = public_name_start + '_' + user_id + '.pem'
    public_list.append(public_name)
for i in range(len(vote_data)):
    generate_rsa_keys(1024,private_list[i],public_list[i])

server_keys = generate_rsa_keys(1024,'server_private.pem','server_public.pem')

def vote_encrypt(vote_list,user):
    """
    Encrypts using the Public Key
    vote_list: a list of the votes to be encrypted
    user: UserID from the JSON in order to use their key to encrypt
    :return: sec_vote -> Encrypted RSA
    """
    user_public_key = RSA.importKey(open(public_list[user]).read())

    encoded_value = []
    for i in range(len(vote_list)):
        d = vote_list[i].encode()
        rook = binascii.hexlify(d)
        encoded_value.append(rook)


    encrypted_vote = []
    for i in range(len(vote_list)):
        vote_ciper = PKCS1_OAEP.new(user_public_key)
        sec_vote = vote_ciper.encrypt(encoded_value[i])
        encrypted_vote.append(sec_vote)

    return encrypted_vote

test_encrypt = vote_encrypt(dummy_vote[0],0)
print(test_encrypt)

def vote_decrypt(encrypted_list, user):
    """
    :param encrypted_list: list containing the encrypted elements
    :param user: the UserID from the JSON
    :return: final_decrypt -> decrypted output
    """
    user_private_key = RSA.importKey(open(private_list[user]).read())

    decrypted_vote = []
    for i in range(len(encrypted_list)):
        vote_plaintext = PKCS1_OAEP.new(user_private_key)
        decrypt_vote = vote_plaintext.decrypt(encrypted_list[i])
        decrypted_vote.append(decrypt_vote)

    decode_vote = []
    for i in range(len(encrypted_list)):
        bishop = binascii.unhexlify(decrypted_vote[i])
        d = bishop.decode()
        decode_vote.append(d)


    final_decrypt = list(map(int, decode_vote))
    return final_decrypt

test_decrypt = vote_decrypt(test_encrypt,0)
print(test_decrypt)


# # Encrypt using AES
# aes_cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv) # CBC Mode AES - for encryption
# ciphered_data = aes_cipher.encrypt(pad(sec_vote, AES.block_size))
# print(ciphered_data)
#
# #Decrypt AES
# aes_plain = AES.new(aes_key, AES.MODE_CBC, aes_iv) # CBC Mode AES - for decryption
# original_sec_vote = unpad(aes_plain.decrypt(ciphered_data), AES.block_size)
# print(original_sec_vote)



# Candidate name - here so i can just copy paste to console : Marcus Maragh




## signature
# h = SHA256.new(vote_sec)
# signature = pss.new(user_private_key).sign(h)
#
# verifier = pss.new(user_public_key)
# try:
#     verifier.verify(h,signature)
#     print("Signature is Authentic")
# except (ValueError,TypeError):
#     print("The signature is not authentic")


