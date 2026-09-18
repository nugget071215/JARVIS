import subprocess
import shutil


def open_app(target):
    if shutil.which(target) is None:
        print(f"I couldn't open {target}. So like... install it dude")
        return

    print(f"Opening {target}....")
    subprocess.Popen([target])

def execute_cmd(cmd):
    if cmd is None:
        print("I don't understand that. PICK YOUR FUCKING CHIN UP CUNT!")
        return
    
    action = cmd["action"]
    target = cmd["target"]

    if action == "open":
        open_app(target)
    elif action == "reboot":
        print("Rebooting! See you soon!")
        subprocess.run(["systemctl", "reboot"])
    elif action == "shutdown":
        print("Shutting down. See you later!")
        subprocess.run(["systemctl", "poweroff"])
    elif action == "lock":
        print("Locking the screen! Catch ya later!")
        subprocess.run(["swaylock"])
    else:
        print(f"I'm kinda useless with this action by the name of... {action}. I'm sleeping with your mom btw.")

