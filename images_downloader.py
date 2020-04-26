import csv
import requests
import os
import errno

file=open('_temp_files/features_temp.csv', "r")
reader = csv.reader(file)
next(reader)        # skip header

for line in reader:
    id = line[0]
    urls = line[-1].split(',')

    for i in range(len(urls)):
        img_data = requests.get(urls[i]).content
        filename = 'images/%s/%d.jpg' % (id, i+1)

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, 'wb') as handler:
            handler.write(img_data)

with open('_temp_files/features_temp.csv', 'r') as fin:
    with open('features.csv', 'w', newline='') as fout:
        writer=csv.writer(fout)
        for row in csv.reader(fin):
            writer.writerow(row[:-1])

