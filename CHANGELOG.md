# Changelog

## v1.0.3
* Added: Check if provided values are string, integer or float
* Changed: Time-To-Go can now be configured in the config file. When charging the battery it's calculating the time to 100% SoC and when discharging it's calculating the time to the SoC configured in the config file.

## v1.0.2
* Added: Timeout in order to disconnect the battery, if no new MQTT message is received after x seconds (configurable in `config.ini`)

## v1.0.1
* Changed: Corrected descriptions in the full JSON structure
* Changed: Fixed division by zero when Current = 0 during calculation of Time-to-Go or Voltage = 0 during calculation of Current (thanks to @xury77 for reporting)

## v1.0.0
* Added: A lot of new values that can be set, check the full [JSON structure](https://github.com/mr-manuel/venus-os_dbus-mqtt-battery#json-structure) in the `README.md` for details
* Added: Device name can be changed in the `config.ini`
* Added: Device instance can be changed in the `config.ini`
* Added: How to create multiple instances in `README.md`
* Changed: ⚠️ JSON key names changed. Pay attention that the keys are case sensitive
* Changed: Completely rewritten the driver to keep it simple with a lot of fields
* Changed: Topic variable name in `config.ini`
* Removed: Alarm settings in `config.ini`. All alarms now have to be triggered over MQTT

## v0.1.0
* Added: Set logging level in `config.ini`
* Added: A lot of new values that can be set, check `README.md` for details
* Changed: Fixed topic name in `config.ini`
* Changed: Logging levels of different messages for clearer output
* Changed: Minimum required data to `power`, `voltage` and `soc`
* Changed: Optimized log output for faster troubleshooting

## v0.0.1
Initial release
