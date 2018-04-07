# indoor-config
Configuracion para el proyecto de raspberry

## Actualizar bluez (bluetooth en linux)
apt-get install libglib2.0-dev libdbus-1-dev libudev-dev libical-dev libreadline6 libreadline6-dev

cd /tmp

wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.49.tar.xz

tar xf bluez-5.49.tar.xz

cd bluez-5.49

./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var 

make

sudo make install

### Esto ya instalo la nueva version, pero hay que hacer que el SO apunte a la misma
sudo vim /lib/systemd/system/bluetooth.service

Make sure the exec.start line points to your new daemon in /usr/libexec/bluetooth

sudo mv /usr/lib/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd-543.orig

sudo ln -s /usr/libexec/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd

sudo systemctl daemon-reload

## Instalacion de librerias para soporte de bluetooth en python
sudo apt-get update

sudo apt-get install libbluetooth-dev bluez bluez-hcidump  libboost-python-dev libboost-thread-dev libglib2.0-dev bluetooth libbluetooth-dev python-pip python-dev ipython

sudo pip install pybluez

### Tambien hay que hacer esto

Running bluetooth in compatibility mode,
by modifying /etc/systemd/system/dbus-org.bluez.service,

changing

ExecStart=/usr/lib/bluetooth/bluetoothd

into

ExecStart=/usr/lib/bluetooth/bluetoothd -C

Then adding the Serial Port Profile, executing:  sudo sdptool add SP
