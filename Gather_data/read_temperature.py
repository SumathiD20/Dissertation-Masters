import time
import board, busio
import adafruit_ds18x20, adafruit_onewire.bus
import csv

# Set up the 1-Wire bus on GPIO4
ow_bus = adafruit_onewire.bus.OneWireBus(board.D4)
sensors = ow_bus.scan()  # list of DS18B20 addresses

# Open CSV file for appending
with open('temperature_log.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['timestamp','temp_C'])

    while True:
        for sensor in sensors:
            temp_c = adafruit_ds18x20.DS18X20(ow_bus, sensor).temperature
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            writer.writerow([timestamp, f"{temp_c:.2f}"])
            print(timestamp, temp_c)
        time.sleep(1)  # wait 1 second
