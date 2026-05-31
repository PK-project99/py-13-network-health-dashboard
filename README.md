# Project 13 — Network Health Dashboard

A Python script that probes network devices and generates a color-coded health report in both CSV and HTML format.

## What it does
- Reads a device inventory from `devices.csv`
- Connects to each device via NAPALM using the NETCONF API
- Pulls live interface and device status data
- Flags unhealthy conditions — recently rebooted (uptime < 5 days), interface down, recent flapping
- Outputs results to `output.csv` and a color-coded `health_report.html` dashboard

## How to run
Populate `devices.csv` with your device details:
```
hostname,ip,username,password,driver
xr-router-01,sandbox-iosxr-1.cisco.com,admin,C1sco12345,iosxr_netconf
```
Then run:
```bash
python health_dashboard.py
```

## Sample output
```
Hostname,Uptime,Recently Rebooted?,Interface,Flapped Recently?,Is Down?
xr-router-01,"1 day, 19:28:03",True,GigabitEthernet0/0/0/0,False,False
xr-router-01,"1 day, 19:28:03",True,GigabitEthernet0/0/0/1,False,False
xr-router-01,"1 day, 19:28:03",True,Loopback0,False,False
xr-router-01,"1 day, 19:28:03",True,MgmtEth0/RP0/CPU0/0,False,False
xr-router-01,"1 day, 19:28:03",True,Null0,False,False
```
![alt text](image.png)
![alt text](image-1.png)

## Concepts used
- `napalm` — vendor-agnostic network device API (`get_facts`, `get_interfaces`)
- NETCONF — open standard protocol used instead of Cisco's older XML agent
- `jinja2` — HTML report generation from a template
- `csv` — device inventory input and report output
- `datetime.timedelta` — human-readable uptime and flap time conversion
- `try/except/finally` with `connection = None` pattern for safe cleanup
- `if __name__ == "__main__"` — standard script entrypoint pattern