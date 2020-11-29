##################################################################################
#### THIS IS JUST FOR ME TO TEST STUFF NOT FOR THE FINAL ITERATION OF PROJECT ####
##################################################################################
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pss


# dummy variables for testing
dummy_ssn = input("Enter your SSN: ")
dummy_vote = input("Enter your preferred Candidate: ")

dummy_ssn = dummy_ssn.encode()
dummy_vote = dummy_vote.encode()

ssn_sec = binascii.hexlify(dummy_ssn)
vote_sec = binascii.hexlify(dummy_vote)

# ssn_return = binascii.unhexlify(ssn_sec)
# vote_return = binascii.unhexlify(vote_sec)


# RSA implementations



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


user_keys = generate_rsa_keys(1024, 'user_private.pem','user_public.pem')
server_keys = generate_rsa_keys(1024,'server_private.pem','server_public.pem')

server_public_key = RSA.importKey(open('server_public.pem').read())
server_private_key = RSA.importKey(open('server_private.pem').read())

user_public_key = RSA.importKey(open('user_public.pem').read())
user_private_key = RSA.importKey(open('user_private.pem').read())

## signature
h = SHA256.new(ssn_sec)
signature = pss.new(user_private_key).sign(h)

verifier = pss.new(user_public_key)
try:
    verifier.verify(h,signature)
    print("Signature is Authentic")
except (ValueError,TypeError):
    print("The signature is not authentic")


