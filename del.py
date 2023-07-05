import subprocess
import os

# Change the current directory to 'web_app'
directory = 'web_app'
os.chdir(directory)

# Run the 'yarn build' command
build_command = 'yarn build'
subprocess.run(build_command, shell=True)

# Change the directory back to the parent directory
os.chdir('..')


import os
import shutil


folders_to_delete = ["build", "dist"]
files_to_delete = [file for file in os.listdir(".") if file.endswith(".spec")]

for folder_name in folders_to_delete:
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        # Directory exists, so delete it recursively
        shutil.rmtree(folder_name)
        print(f"The '{folder_name}' folder has been deleted.")
    else:
        print(f"The '{folder_name}' folder does not exist.")

for file_name in files_to_delete:
    if os.path.isfile(file_name):
        # File exists, so delete it
        os.remove(file_name)
        print(f"The '{file_name}' file has been deleted.")
    else:
        print(f"The '{file_name}' file does not exist.")

# Run the 'pyinstaller' command
command = 'pyinstaller --onefile --add-data "web_app/dist;web_app/dist" P_main.py'
subprocess.run(command, shell=True)

# Run the 'pyinstaller' command
command = 'pyinstaller --onefile --add-data "web_app/dist;web_app/dist" C_main.py'
subprocess.run(command, shell=True)