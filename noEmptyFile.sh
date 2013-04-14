LIMIT=$1
PATTERN=$2

for FILENAME in $(ls | grep "$PATTERN.*\.json") 
do
	FILESIZE=$(stat -c%s "$FILENAME")
	if [ "$FILESIZE" -le "$LIMIT" ]
	then
		rm -f $FILENAME
		echo "File $FILENAME of size $FILESIZE has been removed"
	fi
done

FILESREMAINING=$(ls -la | grep "$PATTERN.*\.json" | wc -l)
echo "$FILESREMAINING files of pattern $PATTERN*.json remaining"
