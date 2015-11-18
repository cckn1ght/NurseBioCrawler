# Find the annotated profiles in the total CSV file
import csv

csvRows = []
shuffled_file = open('shuffledCSV.csv', 'r', encoding='utf-8', errors='ignore')
fileReader = csv.reader(shuffled_file)
annotated_row = 0
for row in fileReader:
    if fileReader.line_num == 1:
        csvRows.append(row)  # Append the first row
    elif row[0] == 'yes' or row[0] == 'no':     # find the annotated line
        csvRows.append(row)
        annotated_row += 1
shuffled_file.close()

csvFileObj2 = open('annotated.csv', 'w', newline='')
csvWriter = csv.writer(csvFileObj2)
for row in csvRows:
    csvWriter.writerow(row)
print(str(annotated_row) + " lines of annotated bios.")
csvFileObj2.close()