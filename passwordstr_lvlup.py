import re
import msvcrt
import sys

def check_feedback(password):
    feedback = []
    if " " in password:
        feedback.append("Password should not contain spaces.")
    if len(password) < 8:
        feedback.append("At least 8 characters.")
    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letter.")
    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letter.")
    if not re.search(r"\d", password):
        feedback.append("Add number.")
    if not re.search(r"[@$!%*?&]", password):
        feedback.append("Add special char (@$!%*?&).")
    return feedback

def clear_console_line():
    # Moves cursor to beginning, clears line
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def password_input_live():
    print("Type your password (press Enter to finish):")
    password = ""
    while True:
        ch = msvcrt.getwch()  # read unicode char
        if ch == '\r':  # Enter pressed
            print()  # move to next line
            break
        elif ch == '\b':  # Backspace pressed
            if len(password) > 0:
                password = password[:-1]
                clear_console_line()
                sys.stdout.write("*" * len(password))
                sys.stdout.flush()
        else:
            password += ch
            sys.stdout.write("*")
            sys.stdout.flush()

        # After each keypress, show feedback
        feedback = check_feedback(password)
        clear_console_line()
        sys.stdout.write("*" * len(password) + "  ")
        if feedback:
            sys.stdout.write("Missing: " + ", ".join(feedback))
        else:
            sys.stdout.write("Strong password!")
        sys.stdout.flush()

    return password

pwd = password_input_live()
print("\nFinal password entered:", pwd)