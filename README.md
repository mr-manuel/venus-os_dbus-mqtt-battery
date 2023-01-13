# dbus-mqtt-battery - Emulates a physical battery from MQTT data

<small>GitHub repository: [mr-manuel/venus-os_dbus-mqtt-battery](https://github.com/mr-manuel/venus-os_dbus-mqtt-battery)</small>

### Disclaimer

I wrote this script for myself. I'm not responsible, if you damage something using my script.


### Purpose

The script emulates a battery in Venus OS. It gets the MQTT data from a subscribed topic and publishes the information on the dbus as the service `com.victronenergy.battery.mqtt_battery` with the VRM instance `41`.


### Config

Copy or rename the `config.sample.ini` to `config.ini` in the `dbus-mqtt-battery` folder and change it as you need it.


### JSON structure

<details><summary>Required data</summary>

```json
{
    "dc": {
        "power": 79.6,
        "voltage": 58.1,
        "current": 1.4,
        "temperature": 23
    },
    "consumed_amphours": 2.9,
    "soc": 99,
    "history": {
        "voltageMin": 0,
        "voltageMax": 0
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
![MQTT Battery - device list - mqtt battery](/screenshots/battery_device_list_mqtt-battery.png)

</details>
