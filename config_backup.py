import schedule
import time
from netmiko import ConnectHandler
from datetime import datetime
import os
from utility_functions import read_csv


def backup_config(device_details):

    device={
        "device_type":"cisco_xr",
        "host":device_details.get("ip"),
        "username":device_details.get("username"),
        "password":device_details.get("password"),
        "port":22
    }
    connection=None
    full_clonfigs=None

    try:
        connection=ConnectHandler(**device)
        full_clonfigs=connection.send_command("show run all")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if(connection):
            connection.disconnect()
            print("Disconnected!!!")


    return full_clonfigs

for device in read_csv("devices.csv"):
    print(device,"\n\n\n\n\n\n*******************")
    print(backup_config(device))

