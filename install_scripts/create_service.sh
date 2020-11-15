#!/bin/bash

cp -a "install_scripts/piplotter.service" /etc/systemd/system
chown root:root /etc/systemd/system/piplotter.service

systemctl daemon-reload
systemctl enable piplotter.service
