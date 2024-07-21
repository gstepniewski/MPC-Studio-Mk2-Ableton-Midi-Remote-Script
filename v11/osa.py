import subprocess

def osa_enter():
    command = "osascript -e 'tell application \"System Events\" to keystroke return'"
    subprocess.run(command, shell=True)