#!/bin/sh

cd /home/ubuntu/WSTM/wstm_project

if [ ! -f ./lock ];
then
	touch ./lock
	echo 
	echo $(date)
	sudo /etc/init.d/tor restart
	sudo python scrap.py
	rm ./lock
fi
