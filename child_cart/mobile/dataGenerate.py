filename = 'textfile.txt'

with open(filename, 'w') as file:
    for i in range(1, 11):
        row = f"[{i},{i},{i}]\n"
        file.write(row)

import os

# Check if the file exists before reading
if not os.path.exists(filename):
    print("File not found.")
else:
    # Get the file size in bytes
    file_size_bytes = os.path.getsize(filename)

    # Convert file size to kilobytes (KB)
    file_size_kb = file_size_bytes / 1024

    print(f"The size of the file '{filename}' is {file_size_kb:.2f} KB.")






