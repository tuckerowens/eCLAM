import csv

def write_csv(target_dir, dataset):
    full_write_name = target_dir + "/" + str(dataset) + '.csv'
    with open(full_write_name, 'w', newline='') as csvfile:
        csvfile.write(dataset.getInfo() + '\n')
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Voltage', 'Current'])
        write_data = zip(dataset.getYUnits(),dataset.getVerticalAt(0))
        for line in write_data:
            writer.writerow(line)
