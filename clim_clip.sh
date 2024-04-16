#!/bin/bash
read -p "Enter first directory: " path
main_dir=$( ls $path )
for DIRECTORY in $main_dir
do 
	echo "$path/$DIRECTORY"
	python3 clim.py  "$path/$DIRECTORY" ./Continents/continents.shp
	way=$path/$DIRECTORY
	for file in $( ls $path/$DIRECTORY/*.tif )
	do
		var=${file#*}
				echo $var
				var="${var%_[12]*.tif}.tif"
				var=${var##*_}
				echo $var
				mv $file $way/${var^}
	done
done

