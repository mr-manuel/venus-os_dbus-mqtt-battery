# Changelog

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
* Added: Set logging level in `config.default.ini`
* Added: A lot of new values that can be set, check `README.md` for details
* Changed: Fixed topic name in `config.ini`
* Changed: Logging levels of different messages for clearer output
* Changed: Minimum required data to `power`, `voltage` and `soc`
* Changed: Optimized log output for faster troubleshooting

## v0.0.1
Initial release
