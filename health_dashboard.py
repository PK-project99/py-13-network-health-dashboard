import csv
from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
from datetime import timedelta



def read_csv(filename):

    devices=[]
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for device_row in reader:
            devices.append(device_row)

    return devices


def get_device_health(device):
    driver = get_network_driver(device["driver"])
    connection = None
    facts={}
    interfaces={}
    
    try:      
        connection = driver(hostname=device["ip"], 
                            username=device["username"], 
                            password=device["password"],
                            optional_args={"hostkey_verify": False}
                            )      
        connection.open()

        facts=connection.get_facts()
        interfaces=connection.get_interfaces()
    
    except Exception as e:
        print(e)
        return None

    finally:
        if connection:
            connection.close()


    return [facts,interfaces]


def extract_health_data(facts, interfaces):

    health_data={"hostname":facts["hostname"],
                 "uptime_raw":facts["uptime"],
                 "uptime_readable":str(timedelta(seconds=facts["uptime"])),
                 "recent_reboot":True if facts["uptime"]<(86400*5) else False,
                 "vendor":facts["vendor"],
                 "os_version":facts["os_version"],
                 "model":facts["model"],
                 "interface_list":facts["interface_list"]
                 }
    for interface in interfaces:

        health_data[interface]={
            "is_up":interfaces[interface]["is_up"],
            "is_enabled":interfaces[interface]["is_enabled"],
            "interface_down_alarm": True if (interfaces[interface]["is_enabled"] and not interfaces[interface]["is_up"] ) else False,
            "description":interfaces[interface]["description"],
            "speed":interfaces[interface]["speed"],
            "last_flapped_raw":interfaces[interface]["last_flapped"],
            "last_flapped_readable":"Never" if interfaces[interface]["last_flapped"]==-1.0 else str(timedelta(seconds=interfaces[interface]["last_flapped"])),
            "flap_alert":True if (interfaces[interface]["last_flapped"]<(86400*5) and interfaces[interface]["last_flapped"] != -1.0 )else False
        }

    return health_data

def write_csv_report(health_data):

    csv_output_rows=[]
       
    for device in health_data:
        for interface in device["interface_list"]:
            csv_output_rows.append({
                "Hostname":device["hostname"],
                "Uptime":device["uptime_readable"],
                "Recently Rebooted?":device["recent_reboot"],
                "Interface":interface,
                "Is Down?": device[interface]["interface_down_alarm"],
                "Flapped Recently?":device[interface]["flap_alert"]

            })

    with open("output.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Hostname","Uptime", "Recently Rebooted?", "Interface", "Flapped Recently?", "Is Down?"])
        writer.writeheader()
        writer.writerows(csv_output_rows)

    return  csv_output_rows

def write_html_report(output_rows):

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('report_template.html')

    html_output=template.render(rows=output_rows)
    
    with open("health_report.html",'w')  as f:
        f.write(html_output)







if __name__ == "__main__":
    device_list= (read_csv("devices.csv"))

    health_data_of_all_devices=[]
    for device in device_list:
        result=get_device_health(device)
        if result:
            health_data=extract_health_data(result[0],result[1])
            health_data_of_all_devices.append(health_data)
        else:
            print(f"Skipping {device["hostname"]} - could not connect")

    csv_output_rows=write_csv_report(health_data_of_all_devices)
    write_html_report(csv_output_rows)

