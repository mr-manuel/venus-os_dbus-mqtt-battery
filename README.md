# dbus-mqtt-battery - Emulates a physical battery from MQTT data

<small>GitHub repository: [mr-manuel/venus-os_dbus-mqtt-battery](https://github.com/mr-manuel/venus-os_dbus-mqtt-battery)</small>

### Disclaimer

I wrote this script for myself. I'm not responsible, if you damage something using my script.


### Purpose

The script emulates a battery in Venus OS. It gets the MQTT data from a subscribed topic and publishes the information on the dbus as the service `com.victronenergy.battery.mqtt_battery` with the VRM instance `41`.


### Config

Copy or rename the `config.sample.ini` to `config.ini` in the `dbus-mqtt-battery` folder and change it as you need it.


### JSON structure

<details><summary>Minimum required</summary>

```json
{
    "dc": {
        "power": 321.6,
        "voltage": 52.7
    },
    "soc": 63
}
```
</details>

<details><summary>Full (with descriptions)</summary>

Please remove the `--> *` comments to get a valid `JSON`. Comments are not allowed in `JSON` structure, but for simplicity I added them.

```json
{
    "dc": {
        "power": 321.6,                 --> Watt
        "voltage": 52.7,                --> Volt
        "current": 6.10,                --> Ampere - if empty, than calculated from "power" and "voltage"
        "temperature": 23               --> Celsius
    },
    "InstalledCapacity": 200.0,         --> Ampere hours - total battery capacity
    "ConsumedAmphours": 74.5,           --> Ampere hours - consumed
    "Capacity": 125.5,                  --> Ampere hours - remaining - if empty, than calculated when "InstalledCapacity" and "ConsumedAmphours" are set
    "soc": 63,                          --> Percent (0-100) - state of charge
    "TimeToGo": 43967,                  --> Seconds - time until the battery is empty - if empty, than calculated when "Capacity" is set or calculated
    "info": {
        "MaxChargeVoltage": 58.4,       --> Volt - Maximum loading voltage that the MultiPlus/Quattro should use
        "MaxChargeCurrent": 80.0,       --> Ampere - Maximum charge current that the MultiPlus/Quattro should use
        "MaxDischargeCurrent": 120.0    --> Ampere - Maximum discharge current that the MultiPlus/Quattro should use
    },
    "history": {
        "ChargeCycles": 5,              --> Number - cycles for complete battery lifetime
        "voltageMin": 40.8,             --> Battery voltage minimum over time
        "voltageMax": 58.4,             --> Battery voltage maximum over time
        "TotalAhDrawn": 1057.3          --> Ampere hours - drawn ampere hours for complete battery lifetime
    },
    "system": {
        "MinVoltageCellId": "C3",       --> String - ID of the cell with the lowest voltage
        "MinCellVoltage": 3.392,        --> Volt - Of the cell with the lowest voltage
        "MaxVoltageCellId": "C15",      --> String - ID of the cell with the highest voltage
        "MaxCellVoltage": 3.417,        --> Volt - Of the cell with the highest voltage
        "MinTemperatureCellId": "C2",   --> String - ID of the cell with the lowest temperature
        "MinCellTemperature": 22.5,     --> Celsius - Of the cell with the lowest temperature
        "MaxTemperatureCellId": "C9",   --> String - ID of the cell with the highest temperature
        "MaxCellTemperature": 23.5      --> Celsius - Of the cell with the highest temperature
    }
}
```
</details>


### Install

1. Copy the `dbus-mqtt-battery` folder to `/data/etc` on your Venus OS device

2. Run `bash /data/etc/dbus-mqtt-battery/install.sh` as root

   The daemon-tools should start this service automatically within seconds.

### Uninstall

Run `/data/etc/dbus-mqtt-battery/uninstall.sh`

### Restart

Run `/data/etc/dbus-mqtt-battery/restart.sh`

### Debugging

The logs can be checked with `tail -n 100 -f /data/log/dbus-mqtt-battery/current | tai64nlocal`

The service status can be checked with svstat `svstat /service/dbus-mqtt-battery`

This will output somethink like `/service/dbus-mqtt-battery: up (pid 5845) 185 seconds`

If the seconds are under 5 then the service crashes and gets restarted all the time. If you do not see anything in the logs you can increase the log level in `/data/etc/dbus-mqtt-battery/dbus-mqtt-battery.py` by changing `level=logging.WARNING` to `level=logging.INFO` or `level=logging.DEBUG`

If the script stops with the message `dbus.exceptions.NameExistsException: Bus name already exists: com.victronenergy.battery.mqtt_battery"` it means that the service is still running or another service is using that bus name.

### Compatibility

It was tested on following devices:

* RaspberryPi 4b
* MultiPlus II (GX Version)

### Screenshots

<details><summary>MQTT Battery</summary>

![MQTT Battery - pages](/screenshots/battery_pages.png)
![MQTT Battery - device list](/screenshots/battery_device_list.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_1.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_2.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_3.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_4.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_5.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_6.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_7.png)

</details>
