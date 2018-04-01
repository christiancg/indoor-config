# indoor-config
Configuracion para el proyecto de raspberry

# Instalacion de librerias para soporte de bluetooth en python
sudo apt-get update

sudo apt-get install libbluetooth-dev bluez bluez-hcidump  libboost-python-dev libboost-thread-dev libglib2.0-dev bluetooth libbluetooth-dev python-pip python-dev ipython

sudo pip install pybluez

## Tambien hay que hacer esto

Running bluetooth in compatibility mode,
by modifying /etc/systemd/system/dbus-org.bluez.service,

changing

ExecStart=/usr/lib/bluetooth/bluetoothd

into

ExecStart=/usr/lib/bluetooth/bluetoothd -C

Then adding the Serial Port Profile, executing:  sudo sdptool add SP
