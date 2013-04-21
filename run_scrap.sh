#!/bin/sh


if [ ! -f ./lock ];
then
	touch ./lock
	sudo /etc/init.d/tor restart
	cd /home/ubuntu/WSTM/wstm_project
	echo >> log
	echo $(date) >> log
	sudo python scrap.py >> log
	rm ./lock
fi
