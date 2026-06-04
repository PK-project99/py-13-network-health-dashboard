import schedule
import time
from netmiko import ConnectHandler
from datetime import datetime
import os
from utility_functions import read_csv


def fetch_backup_config(device_details):

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
        print("Connected!!!")
        full_configs=connection.send_command("show run all")
    except Exception as e:
        print(f"Error: {e}")
        return
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

def run_all_backups(devices_csv):
    devices_list=read_csv(devices_csv)
    for device in devices_list:
        full_config=fetch_backup_config(device)
        if full_config:
            save_to_file(full_config, device.get("hostname"))



if __name__ == "__main__":
    
    while True:
        run_all_backups("devices.csv")
        time.sleep(86400)
