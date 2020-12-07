from flask import Flask, request, jsonify
from Encryption import *

# Generate the Server RSA Keys
server_keys = generate_rsa_keys(2028,'server_private.pem','server_public.pem')

# Generate the IV for AES and respective key
iv_key()
aes_key_iv = read_iv_key()
aes_key = aes_key_iv[:32]
aes_iv = aes_key_iv[32:]

app = Flask(__name__)


@app.route('/vote', methods = ['POST'])
def receive_vote():
    data = request.get_json(force=True)
    payload = data["payload"]
    e_sig = data["e_sig"]

    # needs to decrypt payload and e_sig


    # check that session id's user matches up with SSN and DOB in e-sig
    incorrect_e_sig = False
    # Make sure that user can vote
    unable_to_vote = False
    # Vote

    # If error return 401 for incorrect e_sig, 402 for inability to vote (and descriptive message)
    if incorrect_e_sig:
        return "Invalid E-Signature, either DOB or SSN does not match user's info", 401
    if unable_to_vote:
        return "User has either already voted or is unable to vote.", 402
    # otherwise return 200 status code and a success message
    return "Vote has been placed, thank you.", 200