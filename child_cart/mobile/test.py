data = []
for i in range(1, 81):
    row = [i, i, i]
    data.append(row)

# Write the data to a text file
with open('checkoutData.txt', 'w') as f:
    for row in data:
        line = '[{}, {}, {}]\n'.format(row[0], row[1], row[2])
        f.write(line)

print("Data written to output.txt")
