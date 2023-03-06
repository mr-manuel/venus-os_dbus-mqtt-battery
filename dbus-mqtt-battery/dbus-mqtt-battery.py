#!/usr/bin/env python

from gi.repository import GLib
import platform
import logging
import sys
import os
import time
import json
import paho.mqtt.client as mqtt
import configparser # for config/ini file
import _thread

# import Victron Energy packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'ext', 'velib_python'))
from vedbus import VeDbusService


# get values from config.ini file
try:
    config = configparser.ConfigParser()
    config.read("%s/config.ini" % (os.path.dirname(os.path.realpath(__file__))))
    if (config['MQTT']['broker_address'] == "IP_ADDR_OR_FQDN"):
        print("ERROR:config.ini file is using invalid default values like IP_ADDR_OR_FQDN. The driver restarts in 60 seconds.")
        time.sleep(60)
        sys.exit()
except:
    print("ERROR:config.ini file not found. Copy or rename the config.sample.ini to config.ini. The driver restarts in 60 seconds.")
    time.sleep(60)
    sys.exit()


# Get logging level from config.ini
# ERROR = shows errors only
# WARNING = shows ERROR and warnings
# INFO = shows WARNING and running functions
# DEBUG = shows INFO and data/values
if 'DEFAULT' in config and 'logging' in config['DEFAULT']:
    if config['DEFAULT']['logging'] == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif config['DEFAULT']['logging'] == 'INFO':
        logging.basicConfig(level=logging.INFO)
    elif config['DEFAULT']['logging'] == 'ERROR':
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.WARNING)


# set variables
connected = 0

battery_power = -1
battery_voltage = 0
battery_current = 0
battery_temperature = None

battery_installed_capacity = None
battery_consumed_amphours = None
battery_capacity = None
battery_soc = 0
battery_time_to_go = 0

battery_max_charge_voltage = None
battery_max_charge_current = None
battery_max_discharge_current = None

battery_charge_cycles = None
battery_voltage_min = None
battery_voltage_max = None
battery_total_ah_drawn = None

battery_total_min_voltage_cell_id = None
battery_total_min_cell_voltage = None
battery_total_max_voltage_cell_id = None
battery_total_max_cell_voltage = None

battery_total_min_temperature_cell_id = None
battery_total_min_cell_temperature = None
battery_total_max_temperature_cell_id = None
battery_total_max_cell_temperature = None


# MQTT requests
def on_disconnect(client, userdata, rc):
    global connected
    logging.warning("MQTT client: Got disconnected")
    if rc != 0:
        logging.warning('MQTT client: Unexpected MQTT disconnection. Will auto-reconnect')
    else:
        logging.warning('MQTT client: rc value:' + str(rc))

    try:
        logging.warning("MQTT client: Trying to reconnect")
        client.connect(config['MQTT']['broker_address'])
        connected = 1
    except Exception as e:
        logging.error("MQTT client: Error in retrying to connect with broker: %s" % e)
        connected = 0

def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        logging.info("MQTT client: Connected to MQTT broker!")
        connected = 1
        client.subscribe(config['MQTT']['topic_battery'])
    else:
        logging.error("MQTT client: Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    try:

        global \
            battery_power, battery_voltage, battery_current, battery_temperature, \
            battery_installed_capacity, battery_consumed_amphours, battery_capacity, battery_soc, battery_time_to_go, \
            battery_max_charge_voltage, battery_max_charge_current, battery_max_discharge_current, \
            battery_charge_cycles, battery_voltage_min, battery_voltage_max, battery_total_ah_drawn, \
            battery_total_min_voltage_cell_id, battery_total_min_cell_voltage, battery_total_max_voltage_cell_id, battery_total_max_cell_voltage, \
            battery_total_min_temperature_cell_id, battery_total_min_cell_temperature, battery_total_max_temperature_cell_id, battery_total_max_cell_temperature

        # get JSON from topic
        if msg.topic == config['MQTT']['topic_battery']:
            if msg.payload != '' and msg.payload != b'':
                jsonpayload = json.loads(msg.payload)

                battery_power   = float(jsonpayload["dc"]["power"])
                battery_voltage = float(jsonpayload["dc"]["voltage"])
                battery_current = float(jsonpayload["dc"]["current"]) if 'current' in jsonpayload["dc"] else round( ( float( jsonpayload["dc"]["power"])/float( jsonpayload["dc"]["voltage"]) ), 2 )
                battery_temperature = float(jsonpayload["dc"]["temperature"]) if 'current' in jsonpayload["dc"] else None

                battery_installed_capacity = float(jsonpayload["InstalledCapacity"]) if 'InstalledCapacity' in jsonpayload else None
                battery_consumed_amphours = float(jsonpayload["ConsumedAmphours"]) if 'ConsumedAmphours' in jsonpayload else None
                battery_capacity = float(jsonpayload["Capacity"]) if 'Capacity' in jsonpayload else ( battery_installed_capacity - battery_consumed_amphours ) if battery_installed_capacity is not None and battery_consumed_amphours is not None else None
                battery_soc = int(jsonpayload["soc"])
                battery_time_to_go = int(jsonpayload["TimeToGo"]) if 'TimeToGo' in jsonpayload else round( ( battery_capacity / battery_current * 60 * 60 ), 0 ) if battery_capacity is not None else None

                battery_max_charge_voltage = float(jsonpayload["info"]["MaxChargeVoltage"]) if 'history' in jsonpayload and 'MaxChargeVoltage' in jsonpayload["history"] else None
                battery_max_charge_current = float(jsonpayload["info"]["MaxChargeCurrent"]) if 'history' in jsonpayload and 'MaxChargeCurrent' in jsonpayload["history"] else None
                battery_max_discharge_current = float(jsonpayload["info"]["MaxDischargeCurrent"]) if 'history' in jsonpayload and 'MaxDischargeCurrent' in jsonpayload["history"] else None

                battery_charge_cycles = int(jsonpayload["history"]["ChargeCycles"]) if 'history' in jsonpayload and 'ChargeCycles' in jsonpayload["history"] else None
                battery_voltage_min = float(jsonpayload["history"]["voltageMin"]) if 'history' in jsonpayload and 'voltageMin' in jsonpayload["history"] else None
                battery_voltage_max = float(jsonpayload["history"]["voltageMax"]) if 'history' in jsonpayload and 'voltageMax' in jsonpayload["history"] else None
                battery_total_ah_drawn = float(jsonpayload["history"]["TotalAhDrawn"]) if 'history' in jsonpayload and 'TotalAhDrawn' in jsonpayload["history"] else None

                battery_total_min_voltage_cell_id = jsonpayload["system"]["MinVoltageCellId"] if 'system' in jsonpayload and 'MinVoltageCellId' in jsonpayload["system"] else None
                battery_total_min_cell_voltage = float(jsonpayload["system"]["MinCellVoltage"]) if 'system' in jsonpayload and 'MinCellVoltage' in jsonpayload["system"] else None
                battery_total_max_voltage_cell_id = jsonpayload["system"]["MaxVoltageCellId"] if 'system' in jsonpayload and 'MaxVoltageCellId' in jsonpayload["system"] else None
                battery_total_max_cell_voltage = float(jsonpayload["system"]["MaxCellVoltage"]) if 'system' in jsonpayload and 'MaxCellVoltage' in jsonpayload["system"] else None

                battery_total_min_temperature_cell_id = jsonpayload["system"]["MinTemperatureCellId"] if 'system' in jsonpayload and 'MinTemperatureCellId' in jsonpayload["system"] else None
                battery_total_min_cell_temperature = float(jsonpayload["system"]["MinCellTemperature"]) if 'system' in jsonpayload and 'MinCellTemperature' in jsonpayload["system"] else None
                battery_total_max_temperature_cell_id = jsonpayload["system"]["MaxTemperatureCellId"] if 'system' in jsonpayload and 'MaxTemperatureCellId' in jsonpayload["system"] else None
                battery_total_max_cell_temperature = float(jsonpayload["system"]["MaxCellTemperature"]) if 'system' in jsonpayload and 'MaxCellTemperature' in jsonpayload["system"] else None
            else:
                logging.warning("Received JSON MQTT message was empty and therefore it was ignored")
                logging.debug("MQTT payload: " + str(msg.payload)[1:])

    except ValueError as e:
        logging.error("Received message is not a valid JSON. %s" % e)
        logging.debug("MQTT payload: " + str(msg.payload)[1:])

    except Exception as e:
        logging.error("Exception occurred: %s" % e)
        logging.debug("MQTT payload: " + str(msg.payload)[1:])



class DbusMqttBatteryService:
    def __init__(
        self,
        servicename,
        deviceinstance,
        paths,
        productname='MQTT Battery',
        connection='MQTT Battery service'
    ):

        self._dbusservice = VeDbusService(servicename)
        self._paths = paths

        logging.debug("%s /DeviceInstance = %d" % (servicename, deviceinstance))

        # Create the management objects, as specified in the ccgx dbus-api document
        self._dbusservice.add_path('/Mgmt/ProcessName', __file__)
        self._dbusservice.add_path('/Mgmt/ProcessVersion', 'Unkown version, and running on Python ' + platform.python_version())
        self._dbusservice.add_path('/Mgmt/Connection', connection)

        # Create the mandatory objects
        self._dbusservice.add_path('/DeviceInstance', deviceinstance)
        self._dbusservice.add_path('/ProductId', 0xFFFF)
        self._dbusservice.add_path('/ProductName', productname)
        self._dbusservice.add_path('/CustomName', productname)
        self._dbusservice.add_path('/FirmwareVersion', '0.1.0')
        #self._dbusservice.add_path('/HardwareVersion', '')
        self._dbusservice.add_path('/Connected', 1)

        self._dbusservice.add_path('/Latency', None)

        for path, settings in self._paths.items():
            self._dbusservice.add_path(
                path, settings['initial'], gettextcallback=settings['textformat'], writeable=True, onchangecallback=self._handlechangedvalue
                )

        GLib.timeout_add(1000, self._update) # pause 1000ms before the next request


    def _update(self):
        self._dbusservice['/Dc/0/Power'] =  battery_power # positive: charging, negative: discharging
        self._dbusservice['/Dc/0/Voltage'] = battery_voltage
        self._dbusservice['/Dc/0/Current'] = battery_current
        self._dbusservice['/Dc/0/Temperature'] = battery_temperature

        self._dbusservice['/InstalledCapacity'] = battery_installed_capacity
        self._dbusservice['/ConsumedAmphours'] = battery_consumed_amphours
        self._dbusservice['/Capacity'] = battery_capacity
        self._dbusservice['/Soc'] = battery_soc
        self._dbusservice['/TimeToGo'] = battery_time_to_go

        self._dbusservice['/Info/MaxChargeVoltage'] = battery_max_charge_voltage
        self._dbusservice['/Info/MaxChargeCurrent'] = battery_max_charge_current
        self._dbusservice['/Info/MaxDischargeCurrent'] = battery_max_discharge_current

        # For all alarms: 0=OK; 1=Warning; 2=Alarm
        if battery_voltage == 0:
            alarm_lowvoltage = 0
        elif battery_voltage < float(config['BATTERY']['VoltageLowCritical']):
            alarm_lowvoltage = 2
        elif battery_voltage < float(config['BATTERY']['VoltageLowWarning']):
            alarm_lowvoltage = 1
        else:
            alarm_lowvoltage = 0
        self._dbusservice['/Alarms/LowVoltage'] = alarm_lowvoltage

        if battery_voltage == 0:
            alarm_highvoltage = 0
        elif battery_voltage > float(config['BATTERY']['VoltageHighCritical']):
            alarm_highvoltage = 2
        elif battery_voltage > float(config['BATTERY']['VoltageHighWarning']):
            alarm_highvoltage = 1
        else:
            alarm_highvoltage = 0
        self._dbusservice['/Alarms/HighVoltage'] = alarm_highvoltage

        if battery_soc == 0:
            alarm_lowsoc = 0
        elif battery_soc < float(config['BATTERY']['LowSocCritical']):
            alarm_lowsoc = 2
        elif battery_soc < float(config['BATTERY']['LowSocWarning']):
            alarm_lowsoc = 1
        else:
            alarm_lowsoc = 0
        self._dbusservice['/Alarms/LowSoc'] = alarm_lowsoc

        self._dbusservice['/History/ChargeCycles'] = battery_charge_cycles
        self._dbusservice['/History/MinimumVoltage'] = battery_voltage_min
        self._dbusservice['/History/MaximumVoltage'] = battery_voltage_max
        self._dbusservice['/History/TotalAhDrawn'] = battery_total_ah_drawn

        self._dbusservice['/System/MinVoltageCellId'] = battery_total_min_voltage_cell_id
        self._dbusservice['/System/MinCellVoltage'] = battery_total_min_cell_voltage
        self._dbusservice['/System/MaxVoltageCellId'] = battery_total_max_voltage_cell_id
        self._dbusservice['/System/MaxCellVoltage'] = battery_total_max_cell_voltage

        self._dbusservice['/System/MinTemperatureCellId'] = battery_total_min_temperature_cell_id
        self._dbusservice['/System/MinCellTemperature'] = battery_total_min_cell_temperature
        self._dbusservice['/System/MaxTemperatureCellId'] = battery_total_max_temperature_cell_id
        self._dbusservice['/System/MaxCellTemperature'] = battery_total_max_cell_temperature

        logging.debug("Battery SoC: {:.2f} V - {:.2f} %".format(battery_voltage, battery_soc))


        # increment UpdateIndex - to show that new data is available
        index = self._dbusservice['/UpdateIndex'] + 1  # increment index
        if index > 255:   # maximum value of the index
            index = 0       # overflow from 255 to 0
        self._dbusservice['/UpdateIndex'] = index
        return True

    def _handlechangedvalue(self, path, value):
        logging.debug("someone else updated %s to %s" % (path, value))
        return True # accept the change



def main():
    _thread.daemon = True # allow the program to quit

    from dbus.mainloop.glib import DBusGMainLoop
    # Have a mainloop, so we can send/receive asynchronous calls to and from dbus
    DBusGMainLoop(set_as_default=True)


    # MQTT setup
    client = mqtt.Client("MqttBattery")
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message

    # check tls and use settings, if provided
    if 'tls_enabled' in config['MQTT'] and config['MQTT']['tls_enabled'] == '1':
        logging.info("MQTT client: TLS is enabled")

        if 'tls_path_to_ca' in config['MQTT'] and config['MQTT']['tls_path_to_ca'] != '':
            logging.info("MQTT client: TLS: custom ca \"%s\" used" % config['MQTT']['tls_path_to_ca'])
            client.tls_set(config['MQTT']['tls_path_to_ca'], tls_version=2)
        else:
            client.tls_set(tls_version=2)

        if 'tls_insecure' in config['MQTT'] and config['MQTT']['tls_insecure'] != '':
            logging.info("MQTT client: TLS certificate server hostname verification disabled")
            client.tls_insecure_set(True)

    # check if username and password are set
    if 'username' in config['MQTT'] and 'password' in config['MQTT'] and config['MQTT']['username'] != '' and config['MQTT']['password'] != '':
        logging.info("MQTT client: Using username \"%s\" and password to connect" % config['MQTT']['username'])
        client.username_pw_set(username=config['MQTT']['username'], password=config['MQTT']['password'])

     # connect to broker
    client.connect(
        host=config['MQTT']['broker_address'],
        port=int(config['MQTT']['broker_port'])
    )
    client.loop_start()

    # wait to receive first data, else the JSON is empty and phase setup won't work
    i = 0
    while battery_power == -1:
        if i % 12 != 0 or i == 0:
            logging.info("Waiting 5 seconds for receiving first data...")
        else:
            logging.warning("Waiting since %s seconds for receiving first data..." % str(i * 5))
        time.sleep(5)
        i += 1


    #formatting
    _kwh = lambda p, v: (str(round(v, 2)) + 'kWh')
    _a = lambda p, v: (str(round(v, 2)) + 'A')
    _ah = lambda p, v: (str(round(v, 2)) + 'Ah')
    _w = lambda p, v: (str(round(v, 2)) + 'W')
    _v = lambda p, v: (str(round(v, 2)) + 'V')
    _p = lambda p, v: (str(round(v, 2)) + '%')
    _t = lambda p, v: (str(round(v, 2)) + '°C')
    _n = lambda p, v: (str(round(v, 0)))
    _s = lambda p, v: (str(v))

    paths_dbus = {
        '/Dc/0/Power': {'initial': 0, 'textformat': _w},
        '/Dc/0/Voltage': {'initial': 0, 'textformat': _v},
        '/Dc/0/Current': {'initial': 0, 'textformat': _a},
        '/Dc/0/Temperature': {'initial': None, 'textformat': _t},

        '/InstalledCapacity': {'initial': None, 'textformat': _ah},
        '/ConsumedAmphours': {'initial': None, 'textformat': _ah},
        '/Capacity': {'initial': None, 'textformat': _ah},
        '/Soc': {'initial': 0, 'textformat': _p},
        '/TimeToGo': {'initial': None, 'textformat': _n},

        '/Info/MaxChargeVoltage': {'initial': None, 'textformat': _v},
        '/Info/MaxChargeCurrent': {'initial': None, 'textformat': _a},
        '/Info/MaxDischargeCurrent': {'initial': None, 'textformat': _a},

        '/Alarms/LowVoltage': {'initial': 0, 'textformat': _n},
        '/Alarms/HighVoltage': {'initial': 0, 'textformat': _n},
        '/Alarms/LowSoc': {'initial': 0, 'textformat': _n},
        '/Alarms/HighChargeCurrent': {'initial': 0, 'textformat': _n},
        '/Alarms/HighDischargeCurrent': {'initial': 0, 'textformat': _n},
        '/Alarms/HighCurrent': {'initial': 0, 'textformat': _n},
        '/Alarms/HighChargeTemperature': {'initial': 0, 'textformat': _n},
        '/Alarms/LowChargeTemperature': {'initial': 0, 'textformat': _n},
        '/Alarms/LowCellVoltage': {'initial': 0, 'textformat': _n},
        '/Alarms/LowTemperature': {'initial': 0, 'textformat': _n},
        '/Alarms/HighTemperature': {'initial': 0, 'textformat': _n},

        '/History/ChargeCycles': {'initial': None, 'textformat': _n},
        '/History/MinimumVoltage': {'initial': None, 'textformat': _v},
        '/History/MaximumVoltage': {'initial': None, 'textformat': _v},
        '/History/TotalAhDrawn': {'initial': None, 'textformat': _ah},

        '/System/MinVoltageCellId': {'initial': None, 'textformat': _s},
        '/System/MinCellVoltage': {'initial': None, 'textformat': _v},
        '/System/MaxVoltageCellId': {'initial': None, 'textformat': _s},
        '/System/MaxCellVoltage': {'initial': None, 'textformat': _v},

        '/System/MinTemperatureCellId': {'initial': None, 'textformat': _s},
        '/System/MinCellTemperature': {'initial': None, 'textformat': _t},
        '/System/MaxTemperatureCellId': {'initial': None, 'textformat': _s},
        '/System/MaxCellTemperature': {'initial': None, 'textformat': _t},

        '/System/NrOfModulesOnline': {'initial': 1, 'textformat': _n},
        '/System/NrOfModulesOffline': {'initial': 0, 'textformat': _n},

        '/UpdateIndex': {'initial': 0, 'textformat': _n},
    }


    pvac_output = DbusMqttBatteryService(
        servicename='com.victronenergy.battery.mqtt_battery',
        deviceinstance=41,
        paths=paths_dbus
        )

    logging.info('Connected to dbus and switching over to GLib.MainLoop() (= event based)')
    mainloop = GLib.MainLoop()
    mainloop.run()



if __name__ == "__main__":
  main()
