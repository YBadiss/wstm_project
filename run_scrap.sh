#!/bin/sh

cd /home/ubuntu/WSTM/wstm_project

if [ ! -f ./lock ];
then
	touch ./lock
	filename=$(date +"%Y-%m-%d-%H-%M-%S")
	echo $(date) > ./log/$filename.out
	echo $(date) > ./log/$filename.err
	sudo python scrap.py > ./log/$filename.out 2> ./log/$filename.err
	
	nb_errors=$(cat ./log/$filename.err | wc -l)
	nb_data_errors=$(cat ./log/$filename.err | grep "DataException" | wc -l)
	sudo mail -s "$filename OUT" "yacine.badiss+logs@gmail.com , romain.yon+logs@gmail.com" < ./log/$filename.out
	sudo mail -s "$filename ERR - $nb_data_errors/$nb_errors" "yacine.badiss+logs@gmail.com , romain.yon+logs@gmail.com" < ./log/$filename.err
	rm ./lock
fi
