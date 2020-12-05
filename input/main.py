from data_access import *

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
    user = {
        "Password": password,
        "Name": name,
        "DOB": dob,
        "SSN": ssn
    }
    return jda.insert(user, username)
        
if __name__ == "__main__":
    users_jda = JsonDataAccess("users.json")
    while True:
        print("""
        Actions
        ---------------------------------------------
        1) Create an account
        2) Login
        3) Vote
        """)
        action = input("What would you like to do: ")
        if int(action) not in [1,2,3]:
            print("Action not recognized! Invalid input.")
            continue
        if int(action) == 1:
            print("Create Account")
            username = ""
            while True:
                username = input("What would you like your username to be: ")
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
            print("Login")
        else:
            print("You are not currently logged in, please log in to vote.")
        break
