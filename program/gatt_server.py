from __future__ import print_function
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array

import functools

import configreadwrite
import startstoprestart
import wlanconfig

try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject

from random import randint

import exceptions
import adapters

BLUEZ_SERVICE_NAME = 'org.bluez'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

GATT_MANAGER_IFACE = 'org.bluez.GattManager1'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'



class Application(dbus.service.Object):
    """
    org.bluez.GattApplication1 interface implementation
    """
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)
        self.add_service(ConfigurationService(bus,0))
        self.add_service(StartStopRestartService(bus,1))
        self.add_service(WlanConfigService(bus,2))

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        print('GetManagedObjects')

        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                #~ descs = chrc.get_descriptors()
                #~ for desc in descs:
                    #~ response[desc.get_path()] = desc.get_properties()

        return response
        
	def __del__(self):
		self.remove_from_connection()
		
	@dbus.service.signal(DBUS_PROP_IFACE, signature='sa{sv}as')
	def PropertiesChanged(self, interface, changed, invalidated):
		print('dajhdhjasdhjkadasdas')


class Service(dbus.service.Object):
    """
    org.bluez.GattService1 interface implementation
    """
    PATH_BASE = '/org/bluez/example/service'

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_SERVICE_IFACE: {
                        'UUID': self.uuid,
                        'Primary': self.primary,
                        'Characteristics': dbus.Array(
                                self.get_characteristic_paths(),
                                signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        result = []
        for chrc in self.characteristics:
            result.append(chrc.get_path())
        return result

    def get_characteristics(self):
        return self.characteristics

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_SERVICE_IFACE:
            raise exceptions.InvalidArgsException()

        return self.get_properties()[GATT_SERVICE_IFACE]


class Characteristic(dbus.service.Object):
    """
    org.bluez.GattCharacteristic1 interface implementation
    """
    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + '/char' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_CHRC_IFACE: {
                        'Service': self.service.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                        #~ 'Descriptors': dbus.Array(
                                #~ self.get_descriptor_paths(),
                                #~ signature='o')
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    #~ def add_descriptor(self, descriptor):
        #~ self.descriptors.append(descriptor)

    #~ def get_descriptor_paths(self):
        #~ result = []
        #~ for desc in self.descriptors:
            #~ result.append(desc.get_path())
        #~ return result

    #~ def get_descriptors(self):
        #~ return self.descriptors

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_CHRC_IFACE:
            raise exceptions.InvalidArgsException()

        return self.get_properties()[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_CHRC_IFACE,
                        in_signature='a{sv}',
                        out_signature='ay')
    def ReadValue(self, options):
        print('Default ReadValue called, returning error')
        raise exceptions.NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise exceptions.NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StartNotify(self):
        print('Default StartNotify called, returning error')
        raise exceptions.NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StopNotify(self):
        print('Default StopNotify called, returning error')
        raise exceptions.NotSupportedException()

    @dbus.service.signal(DBUS_PROP_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass

"""

	SERVICIOS QUE PROPIOS

"""
class ConfigurationService(Service):
	CS_UUID = '1266b5fd-b35d-4337-bd61-e2159dfa6633'
	
	def __init__(self, bus, index):
		Service.__init__(self, bus, index, self.CS_UUID, True)
		self.add_characteristic(LeerGpioConfigChrc(bus, 0, self))
		self.add_characteristic(EscribirGpioConfigChrc(bus, 1, self))
		self.add_characteristic(LeerServerConfigChrc(bus, 2, self))
		self.add_characteristic(EscribirServerConfigChrc(bus, 3, self))
		self.add_characteristic(LeerUsersConfigChrc(bus, 4, self))
		self.add_characteristic(EscribirUsersConfigChrc(bus, 5, self))
		
class LeerGpioConfigChrc(Characteristic):
    LEER_GPIO_CONFIG_CHARAC_UUID = '00002a38-0000-1000-8000-00805f9b34fb'
    LECTOR = configreadwrite.ConfigReadWrite()

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.LEER_GPIO_CONFIG_CHARAC_UUID,['read'],service)
		
    def ReadValue(self, options):
        return stringToDbusByteArray(self.LECTOR.readConfigGpio())
        
class LeerServerConfigChrc(Characteristic):
    LEER_SERVER_CONFIG_CHARAC_UUID = '570c9f73-6b43-4adf-90d2-5120b0c20d57'
    LECTOR = configreadwrite.ConfigReadWrite()

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.LEER_SERVER_CONFIG_CHARAC_UUID,['read'],service)
		
    def ReadValue(self, options):
        return stringToDbusByteArray(self.LECTOR.readConfigServer())
        
class LeerUsersConfigChrc(Characteristic):
    LEER_USERS_CONFIG_CHARAC_UUID = '211ae4c5-7df9-4361-9712-f72ee77a7e9b'
    LECTOR = configreadwrite.ConfigReadWrite()

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.LEER_USERS_CONFIG_CHARAC_UUID,['read'],service)
		
    def ReadValue(self, options):
        return stringToDbusByteArray(self.LECTOR.readConfigUsers())

class EscribirGpioConfigChrc(Characteristic):
    ESCRIBIR_GPIO_CONFIG_CHARAC_UUID = '08cf333e-353f-4c82-b0dc-ad2d57d3a018'
    CONFIG_WRITER = configreadwrite.ConfigReadWrite()
    ESTADO = 'error'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.ESCRIBIR_GPIO_CONFIG_CHARAC_UUID,
                ['read','write'],
                service)

    def WriteValue(self, value, options):
		strValue = busByteArrayToString(value)
		self.ESTADO = self.CONFIG_WRITER.writeConfigGpio(strValue)
		
    def ReadValue(self, options):
        return stringToDbusByteArray(self.ESTADO)
        
class EscribirServerConfigChrc(Characteristic):
    ESCRIBIR_SERVER_CONFIG_CHARAC_UUID = 'bdd7bdb8-a503-40cb-b7b0-4114a6d943bc'
    CONFIG_WRITER = configreadwrite.ConfigReadWrite()
    ESTADO = 'error'

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.ESCRIBIR_SERVER_CONFIG_CHARAC_UUID,['read','write'],service)
    
    def WriteValue(self, value, options):
		strValue = busByteArrayToString(value)
		self.ESTADO = self.CONFIG_WRITER.writeConfigServer(strValue)
    
    def ReadValue(self, options):
        return stringToDbusByteArray(self.ESTADO)
        
class EscribirUsersConfigChrc(Characteristic):
    ESCRIBIR_USER_CONFIG_CHARAC_UUID = 'a5b1e27c-a685-41ce-98e2-e361cd122bde'
    CONFIG_WRITER = configreadwrite.ConfigReadWrite()
    ESTADO = 'error'

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.ESCRIBIR_USER_CONFIG_CHARAC_UUID,['read','write'],service)
    
    def WriteValue(self, value, options):
		strValue = busByteArrayToString(value)
		self.ESTADO = self.CONFIG_WRITER.writeConfigUsers(strValue)
    
    def ReadValue(self, options):
        return stringToDbusByteArray(self.ESTADO)
        
class StartStopRestartService(Service):
	SSR_UUID = '45b3dfe8-e976-4928-b671-b11754553d5b'
	
	def __init__(self, bus, index):
		Service.__init__(self, bus, index, self.SSR_UUID, True)
		self.add_characteristic(ServerStatusChrc(bus, 0, self))
		self.add_characteristic(StartStopRestartChrc(bus, 1, self))
		
class ServerStatusChrc(Characteristic):
	SERVER_STATUS_CHARAC_UUID = 'a9d7f22f-5ab4-4d0e-8487-0f5cc6b29bcc'
	READER = startstoprestart.StartStopRestart()
	
	def __init__(self, bus, index, service):
		Characteristic.__init__(self, bus, index,self.SERVER_STATUS_CHARAC_UUID,['read'],service)
		
	def ReadValue(self, options):
		result = self.READER.isServiceRunning()
		return stringToDbusByteArray(str(result))
		
class StartStopRestartChrc(Characteristic):
    START_STOP_RESTART_SERVER_CHARAC_UUID = '00fa5ebb-5093-44cb-b251-cb35c59ded7a'
    WORKER = startstoprestart.StartStopRestart()
    ESTADO = 'error'

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index,self.START_STOP_RESTART_SERVER_CHARAC_UUID,['read','write'],service)
    
    def WriteValue(self, value, options):
	    try:
		    strValue = busByteArrayToString(value)
		    intValue = int(strValue)
		    self.ESTADO = self.WORKER.process(intValue)
	    except Exception, ex:
		    import traceback
		    print(traceback.format_exc())
		    self.ESTADO = self.WORKER.BAD_REQUEST
    
    def ReadValue(self, options):
        return stringToDbusByteArray(self.ESTADO)
        
class WlanConfigService(Service):
	WC_UUID = '2c238ce1-3911-4f28-9b14-07c838d4484d'
	
	def __init__(self, bus, index):
		Service.__init__(self, bus, index, self.WC_UUID, True)
		self.add_characteristic(WlanScanChrc(bus, 0, self))
		self.add_characteristic(WlanGetConnectedChrc(bus, 1, self))
		self.add_characteristic(WlanConnectChrc(bus, 2, self))
		
class WlanScanChrc(Characteristic):
	SCAN_CHARAC_UUID = 'bed8a9ea-9abe-45e1-803f-3f5df41b49fb'
	WLAN = wlanconfig.WlanConfig()
	
	def __init__(self, bus, index, service):
		Characteristic.__init__(self, bus, index,self.SCAN_CHARAC_UUID,['read'],service)
		
	def ReadValue(self, options):
		result = self.WLAN.scanNetworks()
		if result is None:
			result = 'error'
		return stringToDbusByteArray(result)
		
class WlanGetConnectedChrc(Characteristic):
	GET_CONNECTED_CHARAC_UUID = '26e260af-d8f3-42cf-b48e-385eb5af5a9f'
	WLAN = wlanconfig.WlanConfig()
	
	def __init__(self, bus, index, service):
		Characteristic.__init__(self, bus, index,self.GET_CONNECTED_CHARAC_UUID,['read'],service)
		
	def ReadValue(self, options):
		result = self.WLAN.getConnectedNetwork()
		if result is None:
			result = 'error'
		return stringToDbusByteArray(result)
		
class WlanConnectChrc(Characteristic):
	CONNECT_CHARAC_UUID = 'e38f9f14-c984-495f-9eb2-162e2b914a0e'
	ESTADO = 'error'
	WLAN = wlanconfig.WlanConfig()
	
	def __init__(self, bus, index, service):
		Characteristic.__init__(self, bus, index,self.CONNECT_CHARAC_UUID,['read','write'],service)
		
	def WriteValue(self, value, options):
	    try:
		    strValue = busByteArrayToString(value)
		    self.ESTADO = self.WLAN.writeWifiPossibility(strValue)
	    except Exception, ex:
		    import traceback
		    print(traceback.format_exc())
		    self.ESTADO = self.WLAN.BAD_REQUEST
		
	def ReadValue(self, options):
		return stringToDbusByteArray(self.ESTADO)

def stringToDbusByteArray(toConvert):
	result = []
	for letter in toConvert:
		result.append(dbus.Byte(letter))
	return result
	
def busByteArrayToString(toConvert):
	result = ''
	for letter in toConvert:
		result += chr(letter)
	return result

def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(mainloop, error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()

def disconnect(adapter, device):
	print('entro en disconnect')

def gatt_server_main(mainloop, bus, adapter_name):
    adapter = adapters.find_adapter(bus, GATT_MANAGER_IFACE, adapter_name)
    if not adapter:
        raise Exception('GattManager1 interface not found')
	
    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

    app = Application(bus)

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=functools.partial(register_app_error_cb, mainloop))
