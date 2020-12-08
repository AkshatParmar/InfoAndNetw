from data_access import *
from Encryption import *
import os
import binascii
import requests
session = requests.Session()

def password_check(passwd): 
      
    SpecialSym =['$', '@', '#', '%'] 
    val = True
      
    if len(passwd) < 6: 
        print('length should be at least 6') 
        val = False
          
    if len(passwd) > 20: 
        print('length should be not be greater than 8') 
        val = False
          
    if not any(char.isdigit() for char in passwd): 
        print('Password should have at least one numeral') 
        val = False
          
    if not any(char.isupper() for char in passwd): 
        print('Password should have at least one uppercase letter') 
        val = False
          
    if not any(char.islower() for char in passwd): 
        print('Password should have at least one lowercase letter') 
        val = False
          
    if not any(char in SpecialSym for char in passwd): 
        print('Password should have at least one of the symbols $@#') 
        val = False
    if val: 
        return val 

def dob_check(dob):
    digits = '1234567890'
    dob_arr = dob.split("/")
    if len(dob_arr) != 3:
        print(1)
        return False
    
    for dig in ''.join(dob_arr):
        if dig not in digits:
            return False

    if len(dob_arr[0]) != 2:
        print(2)
        return False
    
    if len(dob_arr[1]) != 2:
        print(3)
        return False
    
    if len(dob_arr[2]) != 4:
        print(4)
        return False
    
    return True

def register_user(jda, username, password, name, dob, ssn):

    private_file = username + '_private_key.pem'
    public_file = username + '_public_key.pem'

    generate_rsa_keys(1024, private_file, public_file)

    sec_pass = password.encode()
    sec_pass = binascii.hexlify(sec_pass)
    sec_pass = sec_pass.decode()

    user = {
        "Password": sec_pass,
        "Name": name,
        "DOB": dob,
        "SSN": ssn
    }
    # DOB/SSN/Password all need to be encrypted somehow 

    # Password Encryption in Client Using Users Private/Public Key


    # Encrypt DOB and SSB
    encrypt_ssn = rsa_encryption(ssn,'server')
    encrypt_dob = rsa_encryption(dob,'server')

    # Encrypted Payload as Key, e-signature as the value
    dob_ssn_payload = {
        "SSN": encrypt_ssn , "DOB": encrypt_dob
    }

    # Verifier Payload to be sent to server
    verifier_payload = str(dob_ssn_payload)
    o = session.post("http://localhost:5000/dobssn", json=verifier_payload)

    return jda.insert(user, username)
        
def login(jda, username, password):
    session_jda = JsonDataAccess("sessions.json")
    user_info = jda.search(username)
    if user_info is None:
        return None

    # decrypt password
    decrypted_password = user_info["Password"]
    decrypted_password = decrypted_password.encode()
    decrypted_password = binascii.unhexlify(decrypted_password)
    decrypted_password = decrypted_password.decode()

    if decrypted_password == password:
        #randomly generate a session_id and store that combo with the username somewhere
        while True:
            session_id = binascii.hexlify(os.urandom(16)).decode('utf-8')
            if session_jda.insert({"username":username},session_id):
                break
        return session_id
    
    return None

def logout(session_id):
    session_jda = JsonDataAccess("sessions.json")
    if session_jda.delete(session_id) is False:
        print("Invalid session_id, session was corrupted, please close application and re-run")
    return

def submit_vote(session_id, ssn, dob, votes):
    # Create e signature with ssn and dob
    with open("sessions.json") as file:
        identify = json.load(file)
    user_name = identify[session_id]["username"]
    private_key = user_name + '_private_key.pem'
    e_signature = ssn + dob
    e_signature = signature(e_signature, private_key)


    payload = {
        "SessionID": session_id,
        "Votes": votes
    }

    # RSA encrypt the payload
    payload = str(payload)
    encrypted_payload = rsa_encryption(payload,'server')
    # send payload to server (probably can just use basic flask request for this)
    #print(encrypted_payload, '\n', e_signature) #debug line -- can be removed once everything is added in

    # Encrypted Payload as Key, e-signature as the value
    request_body = {
        "payload": encrypted_payload,
        "e_sig": e_signature
    }

    request_body = str(request_body)
    #print(request_body) # Mainly used as a debugging tool
    r = session.post("http://localhost:5000/vote", json=request_body)

    print(r.text)
    if r.status_code != 200:
        print("Re-run application to attempt to resubmit vote if you believe this was an error.")

if __name__ == "__main__":
    users_jda = JsonDataAccess("users.json")
    session_id = None
    while True:
        print("""
        Actions
        ---------------------------------------------
        1) Create an account
        2) Login
        3) Vote
        """)
        action = input("What would you like to do: ")
        if action not in '1 2 3':
            print("Action not recognized! Invalid input.")
            continue
        if int(action) == 1:
            print("Create Account")
            username = ""
            while True:
                username = input("What would you like your username to be: ")
                # this should probably be abstracted outside of the main logic
                if users_jda.search(username) is None:
                    break
                print("User already created with this username, please try again.")
            password = ""
            while True:
                password = input("What would you like your password to be: ")
                confirm_pasword = input("Re-enter password: ")
                if password == confirm_pasword:
                    if not password_check(password):
                        continue
                    break
                print("Passwords do not match, try again.")
            name = input("What is your name: ")
            while True:
                dob = input("What is your DOB (MM/DD/YYYY): ")
                if not dob_check(dob):
                    print("Invalid DOB, try again.")
                    continue
                break

            while True:
                ssn = input("What is your SSN (no dashes): ")
                if len(ssn) == 9 and ssn.isnumeric():
                    break
                print("Invalid SSN, try again")
            
            if register_user(users_jda, username, password, name, dob, ssn):
                print("Account successfully created")
                break
        elif int(action) == 2:
            attempts = 0
            while attempts < 3: 
                username = input("Username: ")
                password = input("Password: ")
                session_id = login(users_jda, username, password)
                if session_id is not None:
                    print("Success! You are now logged in as:", username)
                    break
                print("Invalid username/password, try again.")
            break
        elif int(action) == 3:
            print("You are not currently logged in, please log in to vote.")
        else:
            break
    
    while session_id is not None:
        print("""
        Actions
        ---------------------------------------------
        1) Vote
        2) Logout
        """)
        action = input("What would you like to do: ")
        if int(action) not in [1,2]:
            print("Action not recognized! Invalid input.")
            continue
        if int(action) == 1:
            president_choice = 0
            state_senator_choice = 0
            print("""
                President
                ----------------------------------------
                1) (R) Donald Trump / Michael Pence
                2) (D) Joe Biden / Kamala Harris
                """)
            while True:
                
                president_choice = input("Choice: ")
                if president_choice in '1 2':
                    break
                print("Invalid choice, try again")
            print("""
                NJ State Senator
                ----------------------------------------
                1) (D) Cory Booker
                2) (D) Lawrence Hamm
                3) (R) Eugene Anagnos 
                4) (R) Tricia Flanagan 
                5) (R) Rik Mehta
                6) (R) Natalie Rivera
                7) (R) Hirsh Singh
                """)
            while True:
                state_senator_choice = input("Choice: ")
                if state_senator_choice in '1 2 3 4 5 6 7':
                    break
                print("Invalid choice, try again")
            dob = None
            ssn = None
            while True:
                dob = input("What is your DOB (MM/DD/YYYY): ")
                if not dob_check(dob):
                    print("Invalid DOB, try again.")
                    continue
                break

            while True:
                ssn = input("What is your SSN (no dashes): ")
                if len(ssn) == 9 and ssn.isnumeric():
                    break
                print("Invalid SSN, try again")
            
            votes = {
                "President": president_choice,
                "NJ State Senator": state_senator_choice
            }

            submit_vote(session_id, ssn, dob, votes)

        elif int(action) == 2:
            logout(session_id)
            session_id = None
        else:
            break

    print("You are not logged into an account, please re-run if you wish to log back in.")