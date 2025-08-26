#write a program to check if i am using github copilot pro or a normal version of github copilot

import os

def check_github_copilot_version():
    # Check if the GitHub Copilot extension is installed
    if "GITHUB_COPILOT_VERSION" in os.environ:
        version = os.environ["GITHUB_COPILOT_VERSION"]
        if version == "pro":
            return "You are using GitHub Copilot Pro."
        else:
            return "You are using the normal version of GitHub Copilot."
    else:
        return "GitHub Copilot is not installed."

print(check_github_copilot_version())