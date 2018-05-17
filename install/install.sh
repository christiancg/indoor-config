# Primero se descarga el repositorio que falta
cd /home/pi
git clone https://github.com/christiancg/indoor.git
# Se copian y habilitan los servicios (se inician mas adelante, faltan dependencias)
sudo cp /home/pi/indoor-config/startup-scripts/indoor-config.service /lib/systemd/system/
sudo cp /home/pi/indoor-config/startup-scripts/indoor.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable indoor.service
sudo systemctl enable indoor-config.service
# Se instalan dependencias de python
sudo pip install flask_sqlalchemy
sudo pip install pika
sudo pip install jsonpickle
sudo pip install pygame
# Actualizacion del driver bluetooth para que ande biene indoor-config
sudo apt-get install -y libglib2.0-dev libdbus-1-dev libudev-dev libical-dev libreadline6 libreadline6-dev
cd /tmp
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.49.tar.xz
tar xf bluez-5.49.tar.xz
cd bluez-5.49
./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var
make
sudo make install
sudo mv /usr/lib/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd-543.orig
sudo ln -s /usr/libexec/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd
sudo systemctl daemon-reload
# Instalacion de librerias para soporte de bluetooth en python
sudo apt-get install -y libbluetooth-dev bluez bluez-hcidump libboost-python-dev libboost-thread-dev libglib2.0-dev bluetooth libbluetooth-dev python-pip python-dev ipython
# Instalacion de libreria de python para bluetooth
sudo pip install pybluez
sudo sed -i -e 's/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd -C/g' /etc/systemd/system/dbus-org.bluez.service
# Agregar el perfil de bluetooth
sudo sdptool add SP
# Actualizar todos los paquetes instalados y reiniciar
sudo apt-get update
sudo apt-get -y upgrade
sudo rpi-update
sudo reboot now
