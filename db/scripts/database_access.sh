#! /bin/sh

select queryfile in *.sql
do 
	cat $queryfile | sqlite3 ../data.db
	echo query is done!
	read -p "Want to proceede? y/n " answer
	echo ""

	if [ $answer == "n" ]; then
		echo -e "this is the end\r\n"
		break
	fi

	i=0
	for file in *.sql; do
		i=$((i+1))
		echo "$i)" $file 
	done

done

