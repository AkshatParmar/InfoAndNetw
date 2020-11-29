##################################################################################
#### THIS IS JUST FOR ME TO TEST STUFF NOT FOR THE FINAL ITERATION OF PROJECT ####
##################################################################################
import binascii
from Crypto.PublicKey import RSA


# dummy variables for testing
#dummy_ssn = input("Enter your SSN: ")
#dummy_vote = input("Enter your preferred Candidate: ")

# dummy_ssn = dummy_ssn.encode()
# dummy_vote = dummy_vote.encode()

# ssn_sec = binascii.hexlify(dummy_ssn)
# vote_sec = binascii.hexlify(dummy_vote)

# ssn_return = binascii.unhexlify(ssn_sec)
# vote_return = binascii.unhexlify(vote_sec)


# RSA implementations



def generate_rsa_keys(modulus, key_type, mod_exp = 65537):
    """
    Function that generates a pair of RSA Keys, and returns either the private or public key depending on the argument
    mod -> RSA modulus length
    mod_exp -> public exponent value. if left blank it defaults to 65537
    key_type -> takes in either 'private' or 'public' to return either the private or public key. If left blank, returns both
    """
    key = RSA.generate(modulus, e=mod_exp)
    private_key = key.exportKey()
    public_key = key.publickey().exportKey()
    if key_type == 'private' or key_type == 'Private':
        return private_key
    elif key_type == 'public' or key_type == 'Public':
        return public_key
    else:
        return private_key, public_key

server_private_key = generate_rsa_keys(1024,'private')
server_public_key = generate_rsa_keys(1024,'public')



