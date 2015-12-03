__author__ = 'Joe'
import csv
import json


with open('predicted.csv', 'r') as input_file:
    input_reader = csv.reader(input_file)
    screen_names = []
    for line in input_reader:
        if input_reader.line_num == 1:
            continue      # skip the first line
        if line[1][2:] == 'yes':
            screen_names.append(line[0])

print (screen_names)
with open('yes_class.json', 'w') as file:
    json.dump(screen_names, file, indent=4)

# with open('yes_class.json', 'r') as jsonfile:
#     x = json.load(jsonfile)
#     for row in x:
#         print(row)