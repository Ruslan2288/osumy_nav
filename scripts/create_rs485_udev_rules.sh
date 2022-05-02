#!/bin/bash

echo "remap the device serial port(ttyUSBX) to  rs485"
echo "RS485 usb connection as /dev/rs485 , check it using the command : ls -l /dev|grep ttyUSB"
echo "start copy RS485.rules to  /etc/udev/rules.d/"
sudo cp `rospack find osumy_nav`/scripts/rs485.rules  /etc/udev/rules.d
echo " "
echo "Restarting udev"
echo ""
sudo service udev reload
sudo service udev restart
echo "finish "
