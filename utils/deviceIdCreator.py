import uuid
import csv

csv_file = "deviceId.csv"

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(["device_id"])

    for _ in range(40000):
        writer.writerow([str(uuid.uuid4())])

# print("100 UUIDs saved to uuid_list.csv")
