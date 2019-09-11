#!/bin/bash
# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
# To uninstall: sudo dpkg -r session-manager-plugin

echo "Downloading session-manager-plugin.deb..."
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"

echo "Installing plugin..."
sudo dpkg -i session-manager-plugin.deb

echo "Cleaning up downloaded file..."
rm session-manager-plugin.deb

echo "Version installed: $(session-manager-plugin --version)"

echo "Enabling logging for the plugin..."

if [ ! -f /usr/local/sessionmanagerplugin/seelog.xml ]; then
  echo "Creating /usr/local/sessionmanagerplugin/seelog.xml..."
  sudo cp /usr/local/sessionmanagerplugin/seelog.xml.template /usr/local/sessionmanagerplugin/seelog.xml

  # Change minlevel="off" to minlevel="info" or minlevel="debug"
  # By default, log entries about opening data channels and reconnecting sessions are recorded at the INFO level.
  # Data flow (packets and acknowledgement) entries are recorded at the DEBUG level.
  sudo sed -i 's/minlevel=\"off\"/minlevel=\"info\"/g' /usr/local/sessionmanagerplugin/seelog.xml
fi

echo "Usage: aws ssm start-session --target <instance-id>"
