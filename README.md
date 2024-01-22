# dbus-mqtt-battery - Emulates a aggregated/physical battery from MQTT data

<small>GitHub repository: [mr-manuel/venus-os_dbus-mqtt-battery](https://github.com/mr-manuel/venus-os_dbus-mqtt-battery)</small>

### Disclaimer

I wrote this script for myself. I'm not responsible, if you damage something using my script.


## Supporting/Sponsoring this project

You like the project and you want to support me?

[<img src="https://github.md0.eu/uploads/donate-button.svg" height="50">](https://www.paypal.com/donate/?hosted_button_id=3NEVZBDM5KABW)


### Purpose

The script emulates a battery in Venus OS. It gets the MQTT data from a subscribed topic and publishes the information on the dbus as the service `com.victronenergy.battery.mqtt_battery` with the VRM instance `41`.

It also can be used to aggregate multiple batteries. In this case you can use Node-RED to read the data from multiple batteries and then feed the calculated data to this driver, which then is selected as battery monitor.


### Config

Copy or rename the `config.sample.ini` to `config.ini` in the `dbus-mqtt-battery` folder and change it as you need it.


### JSON structure

<details><summary>Minimum required to start the driver</summary>

```json
{
    "Dc": {
        "Power": 321.6,
        "Voltage": 52.7
    },
    "Soc": 63
}
```
</details>

<details><summary>Minimum required that the MTTP is controlled by BMS</summary>

```json
{
    "Dc": {
        "Power": 321.6,
        "Voltage": 52.7
    },
    "Soc": 63,
    "Info": {
        "MaxChargeVoltage": 55.2,
        "MaxChargeCurrent": 80,
        "MaxDischargeCurrent": 120
    }
}
```
</details>

<details><summary>Full (with descriptions)</summary>

Please remove the `--> *` comments to get a valid `JSON`. Comments are not allowed in `JSON` structure, but for simplicity I added them.

```json
{
    "Dc": {
        "Power": 321.6,                       --> Watt
        "Voltage": 52.7,                      --> Volt
        "Current": 6.10,                      --> Ampere - if missing in the JSON, than gets calculated from "power" and "voltage"
        "Temperature": 23                     --> Celsius
    },
    "InstalledCapacity": 200.0,               --> Ampere hours - total battery capacity
    "ConsumedAmphours": 74.5,                 --> Ampere hours - consumed (only positive values) - if missing in the JSON, than gets calculated when "InstalledCapacity" and "Capacity" are set OR only "InstalledCapacity" is set
    "Capacity": 125.5,                        --> Ampere hours - remaining (only positive values) - if missing in the JSON, than gets calculated when "InstalledCapacity" and "ConsumedAmphours" are set OR only "InstalledCapacity" is set
    "Soc": 63,                                --> Percent (0-100) - state of charge
    "TimeToGo": 43967,                        --> Seconds - time until the battery is empty - if missing in the JSON, than gets calculated when "Capacity" is set or calculated
    "Balancing": 0,                           --> Int - 0 = inactive; 1 = active
    "SystemSwitch": 0,                        --> Int - 0 = disabled; 1 = enabled
    "Alarms": {
        "LowVoltage": 0,                      --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighVoltage": 0,                     --> Int - 0 = ok; 1 = warning; 2 = alarm
        "LowSoc": 0,                          --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighChargeCurrent": 0,               --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighDischargeCurrent": 0,            --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighCurrent": 0,                     --> Int - 0 = ok; 1 = warning; 2 = alarm
        "CellImbalance": 0,                   --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighChargeTemperature": 0,           --> Int - 0 = ok; 1 = warning; 2 = alarm
        "LowChargeTemperature": 0,            --> Int - 0 = ok; 1 = warning; 2 = alarm
        "LowCellVoltage": 0,                  --> Int - 0 = ok; 1 = warning; 2 = alarm
        "LowTemperature": 0,                  --> Int - 0 = ok; 1 = warning; 2 = alarm
        "HighTemperature": 0,                 --> Int - 0 = ok; 1 = warning; 2 = alarm
        "FuseBlown": 0                        --> Int - 0 = ok; 1 = warning; 2 = alarm
    },
    "Info": {
        "ChargeRequest": 0,                   --> Int - 0 = inactive; 1 = active
        "MaxChargeVoltage": 55.2,             --> Volt - Maximum loading voltage that the MultiPlus/Quattro should use
        "MaxChargeCurrent": 80.0,             --> Ampere - Maximum charge current that the MultiPlus/Quattro should use
        "MaxDischargeCurrent": 120.0          --> Ampere - Maximum discharge current that the MultiPlus/Quattro should use
    },
    "History": {
        "ChargeCycles": 5,                    --> Number - cycles for complete battery lifetime
        "MinimumVoltage": 40.8,               --> Battery voltage minimum over time
        "MaximumVoltage": 58.4,               --> Battery voltage maximum over time
        "TotalAhDrawn": 1057.3                --> Ampere hours - drawn ampere hours for complete battery lifetime
    },
    "System": {
        "MinVoltageCellId": "C3",             --> String - ID of the cell with the lowest voltage - if missing in the JSON, than gets calculated when elements in "Voltages" are present
        "MinCellVoltage": 3.392,              --> Volt - Of the cell with the lowest voltage - if missing in the JSON, than gets calculated when elements in "Voltages" are present
        "MaxVoltageCellId": "C15",            --> String - ID of the cell with the highest voltage - if missing in the JSON, than gets calculated when elements in "Voltages" are present
        "MaxCellVoltage": 3.417,              --> Volt - Of the cell with the highest voltage - if missing in the JSON, than gets calculated when elements in "Voltages" are present

        "MinTemperatureCellId": "C2",         --> String - ID of the cell with the lowest temperature
        "MinCellTemperature": 22.5,           --> Celsius - Of the cell with the lowest temperature
        "MaxTemperatureCellId": "C9",         --> String - ID of the cell with the highest temperature
        "MaxCellTemperature": 23.5,           --> Celsius - Of the cell with the highest temperature
        "MOSTemperature": 23.5,               --> Celsius - Temperature of the Mosfets

        "NrOfModulesOnline": 0,               --> Number - How many modules are online
        "NrOfModulesOffline": 0,              --> Number - How many modules are offline

        "NrOfModulesBlockingCharge": 0,       --> Number - How many modules are blocking charge
        "NrOfModulesBlockingDischarge": 0     --> Number - How many modules are blocking discharge
    },
    "Voltages": {
        "Cell1":  3.201,                      --> Volt - voltage of this cell
        "Cell2":  3.202,                      --> Volt - voltage of this cell
        "Cell3":  3.203,                      --> Volt - voltage of this cell
        "Cell4":  3.204,                      --> Volt - voltage of this cell
        "Cell5":  3.205,                      --> Volt - voltage of this cell
        "Cell6":  3.206,                      --> Volt - voltage of this cell
        "Cell7":  3.207,                      --> Volt - voltage of this cell
        "Cell8":  3.208,                      --> Volt - voltage of this cell
        "Cell9":  3.209,                      --> Volt - voltage of this cell
        "Cell10": 3.210,                      --> Volt - voltage of this cell
        "Cell11": 3.211,                      --> Volt - voltage of this cell
        "Cell12": 3.212,                      --> Volt - voltage of this cell
        "Cell13": 3.213,                      --> Volt - voltage of this cell
        "Cell14": 3.214,                      --> Volt - voltage of this cell
        "Cell15": 3.215,                      --> Volt - voltage of this cell
        "Cell16": 3.216,                      --> Volt - voltage of this cell
        "Cell17": 3.217,                      --> Volt - voltage of this cell
        "Cell18": 3.218,                      --> Volt - voltage of this cell
        "Cell19": 3.219,                      --> Volt - voltage of this cell
        "Cell20": 3.220,                      --> Volt - voltage of this cell
        "Cell21": 3.221,                      --> Volt - voltage of this cell
        "Cell22": 3.222,                      --> Volt - voltage of this cell
        "Cell23": 3.223,                      --> Volt - voltage of this cell
        "Cell24": 3.224                       --> Volt - voltage of this cell
    },
    "Balances": {
        "Cell1":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell2":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell3":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell4":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell5":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell6":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell7":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell8":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell9":  0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell10": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell11": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell12": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell13": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell14": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell15": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell16": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell17": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell18": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell19": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell20": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell21": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell22": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell23": 0,                          --> Int - 0 = inactive; 1 = cell is beeing balanced
        "Cell24": 0                           --> Int - 0 = inactive; 1 = cell is beeing balanced
    },
    "Io": {
        "AllowToCharge": 0,                   --> Int - 0 = disabled; 1 = enabled
        "AllowToDischarge": 0,                --> Int - 0 = disabled; 1 = enabled
        "AllowToBalance": 0,                  --> Int - 0 = disabled; 1 = enabled
        "ExternalRelay": 0                    --> Int - 0 = disabled; 1 = enabled
    }
}
```
</details>


### Install

1. Login to your Venus OS device via SSH. See [Venus OS:Root Access](https://www.victronenergy.com/live/ccgx:root_access#root_access) for more details.

2. Execute this commands to download and extract the files:

    ```bash
    # change to temp folder
    cd /tmp

    # download driver
    wget -O /tmp/venus-os_dbus-mqtt-battery.zip https://github.com/mr-manuel/venus-os_dbus-mqtt-battery/archive/refs/heads/master.zip

    # If updating: cleanup old folder
    rm -rf /tmp/venus-os_dbus-mqtt-battery-master

    # unzip folder
    unzip venus-os_dbus-mqtt-battery.zip

    # If updating: backup existing config file
    mv /data/etc/dbus-mqtt-battery/config.ini /data/etc/dbus-mqtt-battery_config.ini

    # If updating: cleanup existing driver
    rm -rf /data/etc/dbus-mqtt-battery

    # copy files
    cp -R /tmp/venus-os_dbus-mqtt-battery-master/dbus-mqtt-battery/ /data/etc/

    # If updating: restore existing config file
    mv /data/etc/dbus-mqtt-battery_config.ini /data/etc/dbus-mqtt-battery/config.ini
    ```

3. Copy the sample config file, if you are installing the driver for the first time and edit it to your needs.

    ```bash
    # copy default config file
    cp /data/etc/dbus-mqtt-battery/config.sample.ini /data/etc/dbus-mqtt-battery/config.ini

    # edit the config file with nano
    nano /data/etc/dbus-mqtt-battery/config.ini
    ```

4. Run `bash /data/etc/dbus-mqtt-battery/install.sh` to install the driver as service.

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

### Multiple instances

It's possible to have multiple instances, but it's not automated. Follow these steps to achieve this:

1. Save the new name to a variable `driverclone=dbus-mqtt-battery-2`

2. Copy current folder `cp -r /data/etc/dbus-mqtt-battery/ /data/etc/$driverclone/`

3. Rename the main script `mv /data/etc/$driverclone/dbus-mqtt-battery.py /data/etc/$driverclone/$driverclone.py`

4. Fix the script references for service and log
    ```
    sed -i 's:dbus-mqtt-battery:'$driverclone':g' /data/etc/$driverclone/service/run
    sed -i 's:dbus-mqtt-battery:'$driverclone':g' /data/etc/$driverclone/service/log/run
    ```

5. Change the `device_name` and increase the `device_instance` in the `config.ini`

Now you can install and run the cloned driver. Should you need another instance just increase the number in step 1 and repeat all steps.


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
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_8.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_9.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_10.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_11.png)
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery_12.png)

</details>
