for folder in $(ls)
do
	if [ -d "$folder" ]
	then
		rename "s/\.json$//" $folder/next_hit.json
	fi
done
