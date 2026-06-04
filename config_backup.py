import schedule
import time
from netmiko import ConnectHandler
from datetime import datetime
import os
from utility_functions import read_csv


def backup_config(device_details):

    device={
        "device_type":device_details.get("netmiko_driver"),
        "host":device_details.get("ip"),
        "username":device_details.get("username"),
        "password":device_details.get("password"),
        "port":22
    }
    connection=None
    full_configs=None

    try:
        connection=ConnectHandler(**device)
        full_configs=connection.send_command("show run all")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.disconnect()
            print("Disconnected!!!")


    return full_configs

def save_to_file(full_config, hostname):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("backups", exist_ok=True) #this creates a folder. exist_ok=True is to tell that dont create a directory if one already exists. Otherwise it'll throw an error.
    filename=f"backups/{hostname}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(full_config)
    print(f"Configs saved in {filename}")


for device in read_csv("devices.csv"):
    print(device,"\n\n\n\n\n\n*******************")
    fullconfig=(backup_config(device))
    if fullconfig:
        save_to_file(fullconfig, device.get("hostname"))

