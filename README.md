# dbus-mqtt-battery - Emulates a aggregated/physical battery from MQTT data

<small>GitHub repository: [mr-manuel/venus-os_dbus-mqtt-battery](https://github.com/mr-manuel/venus-os_dbus-mqtt-battery)</small>

## Index

1. [Disclaimer](#disclaimer)
1. [Supporting/Sponsoring this project](#supportingsponsoring-this-project)
1. [Purpose](#purpose)
1. [Config](#config)
1. [JSON structure](#json-structure)
    - [Generic device](#generic-device)
    - [dbus-serialbattery](#dbus-serialbattery)
1. [Install / Update](#install--update)
1. [Uninstall](#uninstall)
1. [Restart](#restart)
1. [Debugging](#debugging)
1. [Compatibility](#compatibility)
1. [Screenshots](#screenshots)


## Disclaimer

I wrote this script for myself. I'm not responsible, if you damage something using my script.


## Supporting/Sponsoring this project

You like the project and you want to support me?

[<img src="https://github.md0.eu/uploads/donate-button.svg" height="50">](https://www.paypal.com/donate/?hosted_button_id=3NEVZBDM5KABW)


## Purpose

The script emulates a battery in Venus OS. It gets the MQTT data from a subscribed topic and publishes the information on the dbus as the service `com.victronenergy.battery.mqtt_battery` with the VRM instance `41`.

It also can be used to aggregate multiple batteries. In this case you can use Node-RED to read the data from multiple batteries and then feed the calculated data to this driver, which then is selected as battery monitor.


## Config

Copy or rename the `config.sample.ini` to `config.ini` in the `dbus-mqtt-battery` folder and change it as you need it.


## JSON structure

### Generic device

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
    "Soh": 98,                                --> Percent (0-100) - state of health
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
        "MaxDischargeCurrent": 120.0,         --> Ampere - Maximum discharge current that the MultiPlus/Quattro should use
        "MaxChargeCellVoltage": 3.65,         --> Volt - Maximum cell voltage for charging
        "HeatingCurrent": 10.0,               --> Ampere - Current used for heating
        "HeatingPower": 120.0,                --> Watt - Power used for heating
        "HeatingTemperatureStart": 5.0,       --> Celsius - Temperature to start heating
        "HeatingTemperatureStop": 10.0        --> Celsius - Temperature to stop heating
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
        "NrOfCellsPerBattery: 0,              --> Number - How many celle are in the battery

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
        "AllowToHeat": 0,                     --> Int - 0 = disabled; 1 = enabled
        "ExternalRelay": 0                    --> Int - 0 = disabled; 1 = enabled
    },
    "Heating": 0,                             --> Int - 0 = inactive; 1 = heating active
    "TimeToSoC": {                            --> Object - time to reach certain SoC levels (in seconds)
        "0": 0,
        "5": 0,
        "10": 0,
        "15": 0,
        "20": 0,
        "25": 0,
        "30": 0,
        "35": 0,
        "40": 0,
        "45": 0,
        "50": 0,
        "55": 0,
        "60": 0,
        "65": 0,
        "70": 0,
        "75": 0,
        "80": 0,
        "85": 0,
        "90": 0,
        "95": 0,
        "100": 0
    }
}
```

</details>

### dbus-serialbattery

If you want to get the values from [`dbus-serialbattery`](https://github.com/mr-manuel/venus-os_dbus-serialbattery) without having to modify any data with Node-RED or other scripts, then with [`dbus-serialbattery`](https://github.com/mr-manuel/venus-os_dbus-serialbattery) version `v2.0.20241223dev` (or later) and `dbus-mqtt-battery` version `v1.0.10-dev (20241223)` (or later) this is easily possible.

To achieve this you need to:

1. Make sure to enable `PUBLISH_BATTERY_DATA_AS_JSON` in the `dbus-serialbattery` [`config.ini`](https://github.com/mr-manuel/venus-os_dbus-serialbattery/blob/f769aebeac3eb7a51b5f9c4e26ac3dd422d42eff/dbus-serialbattery/config.default.ini#L461-L463), since it's disabled by default. Restart `dbus-serialbattery` after you made the changes.

   Now all battery data for each battery is published to its own topic: `/N/<VRM_ID>/battery/<BATTERY_INSTANCE>/JsonData`. Replace `<VRM_ID>` with your VRM ID and  `<BATTERY_INSTANCE>` with the unique instance ID for that battery (one topic per battery).
2. In the `config.ini` of `dbus-mqtt-battery` set the Venus MQTT broker and the topic `/N/<VRM_ID>/battery/<BATTERY_INSTANCE>/JsonData` where the data is published.

Replace the placeholders `<...>` with your values.

This method will fetch automatically all available data for a specific battery from `dbus-serialbattery`. You cannot choose which data you need or not.

## Install / Update

1. Login to your Venus OS device via SSH. See [Venus OS:Root Access](https://www.victronenergy.com/live/ccgx:root_access#root_access) for more details.
2. Execute this commands to download and copy the files:

    ```bash

    wget -O /tmp/download_dbus-mqtt-battery.sh https://raw.githubusercontent.com/mr-manuel/venus-os_dbus-mqtt-battery/master/download.sh

    bash /tmp/download_dbus-mqtt-battery.sh

    ```
3. Select the version you want to install.
4. Press enter for a single instance. For multiple instances, enter a number and press enter.

    Example:

   - Pressing enter or entering `1` will install the driver to `/data/etc/dbus-mqtt-battery`.
   - Entering `2` will install the driver to `/data/etc/dbus-mqtt-battery-2`.

### Extra steps for your first installation

5. Edit the config file to fit your needs. The correct command for your installation is shown after the installation.

   - If you pressed enter or entered `1` during installation:

    ```bash

    nano /data/etc/dbus-mqtt-battery/config.ini

    ```

   - If you entered `2` during installation:

    ```bash

    nano /data/etc/dbus-mqtt-battery-2/config.ini

    ```
6. Install the driver as a service. The correct command for your installation is shown after the installation.

   - If you pressed enter or entered `1` during installation:

    ```bash

    bash /data/etc/dbus-mqtt-battery/install.sh

    ```

   - If you entered `2` during installation:

    ```bash

    bash /data/etc/dbus-mqtt-battery-2/install.sh

    ```

    The daemon-tools should start this service automatically within seconds.

## Uninstall

⚠️ If you have multiple instances, ensure you choose the correct one. For example:

- To uninstall the default instance:

    ```bash

    bash /data/etc/dbus-mqtt-battery/uninstall.sh

    ```
- To uninstall the second instance:

    ```bash

    bash /data/etc/dbus-mqtt-battery-2/uninstall.sh

    ```

## Restart

⚠️ If you have multiple instances, ensure you choose the correct one. For example:

- To restart the default instance:

    ```bash

    bash /data/etc/dbus-mqtt-battery/restart.sh

    ```
- To restart the second instance:

    ```bash

    bash /data/etc/dbus-mqtt-battery-2/restart.sh

    ```

## Debugging

⚠️ If you have multiple instances, ensure you choose the correct one.

- To check the logs of the default instance:

    ```bash

    tail -n 100 -F /data/log/dbus-mqtt-battery/current | tai64nlocal

    ```
- To check the logs of the second instance:

    ```bash

    tail -n 100 -F /data/log/dbus-mqtt-battery-2/current | tai64nlocal

    ```

The service status can be checked with svstat `svstat /service/dbus-mqtt-battery`

This will output somethink like `/service/dbus-mqtt-battery: up (pid 5845) 185 seconds`

If the seconds are under 5 then the service crashes and gets restarted all the time. If you do not see anything in the logs you can increase the log level in `/data/etc/dbus-mqtt-battery/dbus-mqtt-battery.py` by changing `level=logging.WARNING` to `level=logging.INFO` or `level=logging.DEBUG`

If the script stops with the message `dbus.exceptions.NameExistsException: Bus name already exists: com.victronenergy.battery.mqtt_battery"` it means that the service is still running or another service is using that bus name.

## Compatibility

This software supports the latest three stable versions of Venus OS. It may also work on older versions, but this is not guaranteed.

## Screenshots

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
