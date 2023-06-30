import os

folders_to_delete = ["build", "dist"]
files_to_delete = [file for file in os.listdir(".") if file.endswith(".spec")]

for folder_name in folders_to_delete:
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        # Directory exists, so delete it
        os.rmdir(folder_name)
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
