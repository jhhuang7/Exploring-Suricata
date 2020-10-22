while :
do
	now=$(date +"%H:%M:%S.%N")
	curl 10.0.0.4
	now2=$(date +"%H:%M:%S.%N")
	echo "$now to $now2"
	echo "$now to $now2" >> log.txt
	sleep 0.5
done