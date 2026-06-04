import csv 
def read_csv(filename):

    devices=[]
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for device_row in reader:
            devices.append(device_row)

    return devices

