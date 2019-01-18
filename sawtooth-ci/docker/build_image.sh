#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "ERROR: Too few arguments."
	echo
	echo "USAGE: ./build_image.sh <dockerfilename>"
	echo
	echo "<dockerfilename> : the name of the Dockerfile you'd like to build."
	echo -e '\t\t   This is also the name that the image will be tagged with.'
	exit 1
fi

docker build -t $1 -f $1 .