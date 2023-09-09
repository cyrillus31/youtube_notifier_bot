#! /bin/sh

echo -e "\nWhat sort of query do you want to run? See the following options:\n"

select queryfile in *.sql
do 
	# run the query
	cat $queryfile | sqlite3 ../data.db
	echo ""
	echo The query is done!
	echo ""
	
	# ask if the user wants to search again
	read -p "Do you want to search again? y/n: " answer
	echo ""

	if [ $answer == "n" ]; then
		echo -e "The script is being terminated\r\n"
		break 

	elif [ $answer == "y" ]; then
		true # pass
	else
		echo -e "I don't understand you. "
		echo -e "Try again\r\n"
		break
	fi
	
	# print the list of available queries
	i=0
	for file in *.sql; do
		i=$((i+1))
		echo "$i) $file"
	done

done

