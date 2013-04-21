#!/bin/sh

sudo /etc/init.d/tor restart
cd /home/ubuntu/WSTM/wstm_project
echo >> log
echo $(date) >> log
sudo python scrap.py >> log
