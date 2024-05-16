import subprocess


venv_name = "nqa_venv"
commands = [
    f"python -m venv {venv_name}",
    "deactivate",
    f"./{venv_name}/Scripts/activate",
    "pip install -r requirements.txt",
    "echo only if your pip installation is success then run the below command!!!!!"
    "python app.py"
]

for command in commands[0:1]:
    try:
        subprocess.run(command, shell=True)
        print(f"{command} executed successfully!")

    except subprocess.CalledProcessError:
        print(f"{command} execution failed!")
        print(f"try again after deleting {venv_name} folder")
        break

print("")
print("now you have to copy paste these commands on the same terminal line by line")
print("")
for line, command in enumerate(commands[1:], start=1):
    print(line, ".)", command)
