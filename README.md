# Info and Network Security Voting Assignment
## Group 12

### How to Run
1) Download all python packages necessary to run the application
```
pip install requests flask matplotlib pycryptodome
```
2) Open codebase folder and run whitelist file to add usernames who can vote to the whitelist
3) Then run the main python file and server python file simultaneously
```
python main.py
```
Separate terminal window:
```
export FLASK_APP=server.py
flask run
```
4) Now you can operate the client as you'd like
5) In order to see the analysis, run:
```
python Analysis.py
```
 - This will generate the voting graphs
