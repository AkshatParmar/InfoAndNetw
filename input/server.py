from flask import Flask, request, jsonify
import ast
from Encryption import *
from data_access import *

# Generate the Server RSA Keys
generate_rsa_keys(2048,'server_private.pem','server_public.pem')

# Generate the IV for AES and respective key
iv_key()
aes_key_iv = read_iv_key()
aes_key = aes_key_iv[:32]
aes_iv = aes_key_iv[32:]

app = Flask(__name__)

@app.route('/dobssn', methods= ['POST'])
def receive_register(voteJSON, e_sig):
    print("VOTE: ")
    print(voteJSON)

    # Check session eligibility: check that session id's 
        # user matches up with SSN and DOB in e-sig
    sessions_jda = JsonDataAccess("sessions.json")
    userPair = sessions_jda.search(voteJSON["SessionID"])
    
    if userPair is None:
        return -1

    username = userPair["username"]

    # Now that we have the username of the voter,
        # we match their SSN & DOB
    users_jda = JsonDataAccess("users.json")
    userInfo = users_jda.search(username)
    
    if (userInfo["DOB"] != e_sig[1] or userInfo["SSN"] != e_sig[0]): # SSN/DOB don't match
        return -1

    # Whitelist check
    whitelist_jda = JsonDataAccess("whitelist.json")
    whitelist_jda.insert(True, username) # SETUP: keep for population, comment out later

    if whitelist_jda.search(username) is None: # User can't vote
        return -2
    
    # Vote Input ==> votes.json
    votes_jda = JsonDataAccess("votes.json")
    president_arr = votes_jda.search("President")
    senator_arr = votes_jda.search("NJ State Senator")
    
    # (One-time) votes.json setup
    if (president_arr is None):
        votes_jda.insert([], "President")
        votes_jda.insert([], "NJ State Senator")
        president_arr = votes_jda.search("President")
        senator_arr = votes_jda.search("NJ State Senator")

    presChoice = voteJSON["Votes"]["President"]
    senChoice = voteJSON["Votes"]["NJ State Senator"]
    
    if presChoice == "1":
        president_arr.append((username,"Donald Trump"))
    else: # presChoice == "2":
        president_arr.append((username, "Joe Biden"))   
    votes_jda.update(president_arr, "President")

    if senChoice == "1":
        senator_arr.append((username, "Cory Booker"))
    elif senChoice == "2":
        senator_arr.append((username, "Lawrence Hamm"))
    elif senChoice == "3":
        senator_arr.append((username, "Eugene Anagnos"))
    elif senChoice == "4":
        senator_arr.append((username, "Tricia Flanagan"))
    elif senChoice == "5":
        senator_arr.append((username, "Rik Mehta"))
    elif senChoice == "6":
        senator_arr.append((username, "Natalie Rivera"))
    else: # senChoice == "7":
        senator_arr.append((username, "Hirsh Singh"))
    votes_jda.update(senator_arr, "NJ State Senator")

    # Remove username from whitelist (voted)
    whitelist_jda.delete(username) # SETUP: comment out to populate whitelist

def vote_tally():
    votes_jda = JsonDataAccess("votes.json")
    president_arr = votes_jda.search("President")
    senator_arr = votes_jda.search("NJ State Senator")

    presTally = dict()
    senTally = dict()

    for vote in president_arr:
        presTally[vote[1]] = presTally.get(vote[1], 0) + 1

    for vote in senator_arr:
        senTally[vote[1]] = senTally.get(vote[1], 0) + 1

    print(presTally)
    print(senTally)
    return [presTally, senTally]

@app.route('/vote', methods = ['POST'])
def receive_vote():
    data = request.get_json(force=True)
    data = ast.literal_eval(data)

    payload = data["payload"]
    e_sig = data['e_sig']
    vote_dict = rsa_decryption(payload, 'server')
    e_sig = rsa_decryption(e_sig,'server')
    e_sig = e_sig.split("_")
    # print(e_sig)
    vote_dict = ast.literal_eval(vote_dict)

    procExit = receive_register(vote_dict, e_sig)

    # check that session id's user matches up with SSN and DOB in e-sig
    incorrect_e_sig = False
    if (procExit == -1):
        incorrect_e_sig = True
    # Make sure that user can vote
    unable_to_vote = False
    if (procExit == -2):
        unable_to_vote = True

    # Display vote tally server-side
    print("--CURRENT TALLY--")
    vote_tally()

    # If error return 401 for incorrect e_sig, 402 for inability to vote (and descriptive message)
    if incorrect_e_sig:
        return "Invalid E-Signature: DOB, SSN and/or session ID does not match user's info", 401
    if unable_to_vote:
        return "User has either already voted or is unable to vote.", 402
    # otherwise return 200 status code and a success message
    return "Vote has been placed, thank you.", 200

if __name__ == "__main__":
    app.debug = True
    app.run()