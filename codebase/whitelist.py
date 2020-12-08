from data_access import *

if __name__ == "__main__":
    whitelist_jda = JsonDataAccess("whitelist.json")
    username = ""
    print("""
    Whitelist Creator
    ---------------------------------
    """)
    while True:
        username = input("Type username to add to whitelist or exit to exit: ")
        if 'exit' in username:
            break
        if whitelist_jda.insert(True, username) is False:
            print("Error with last user, user already whitelisted.")