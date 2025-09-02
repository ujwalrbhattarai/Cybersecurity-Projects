import re
import msvcrt
import sys

def check_feedback(password):
    feedback=[]
    if " " in password:
        feedback.append("mustnot contain spaces")
    if len(password)<8:
        feedback.append("must be 8 char long")
    if not re.search(r"[A-z]",password):
        feedback.append("must contain at least 1 uppercase ")
    if not re.search(r"[a-z]",password):
        feedback.append("must contain at least one lowercase")
    if not re.search(r"\d",password):
        feedback.append("must contain one digit")
    if not re.search(r"[!@#$%^&*_]",password):
        feedback.append("must contain at least one special character")
    
    return feedback

def clr_console_line():
    sys.stdout.write('\r'+' '*80+'\r')
    sys.stdout.flush()

def live_inp():
    print("input your password and hit enter to confirm")
    password=""
    while True:
        ch=msvcrt.getwch()

        if ch=='\r':
            print()
            break
        
        elif ch=='\b':
            if len(password)>0:
                password=password[:-1]
                clr_console_line()
                sys.stdout.write("*" * len(password))
                sys.stdout.flush()
        else:
            password+=ch
            sys.stdout.write("*")
            sys.stdout.flush()
            #clr_console_line()

        feedback=check_feedback(password)
        clr_console_line()
        sys.stdout.write("*"*len(password)+" ")

        if feedback:
            sys.stdout.write("missing:"+",".join(feedback))

        else:
            sys.stdout.write("strong password")
        sys.stdout.flush()

    return password

pwd = live_inp()
print("the password you've entered is:",pwd)
