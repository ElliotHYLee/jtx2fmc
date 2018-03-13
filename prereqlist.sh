#!/bin/sh


# for pymavlink & dronekit
sudo pip2 install serial
sudo pip2 install pyserial  #without this, serial.Serial no module no component error
sudo pip3 install serial
sudo pip3 install pyserial

sudo pip2 install dronekit
sudo pip2 install dronekit-sitl
sudo pip3 install dronekit
sudo pip3 install dronekit-sitl


#install pymav manually(newr version)
cd ..
git clone --recursive https://github.com/ArduPilot/mavlink
cd mavlink/pymavlink

sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo pip2 install -U future lxml
sudo pip3 install -U future lxml

sudo python2 setup.py install
sudo python3 setup.py install

