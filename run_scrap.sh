#!/bin/sh

sudo /etc/init.d/tor restart
echo $(date) >> log
sudo ./scrap.py >> log 
