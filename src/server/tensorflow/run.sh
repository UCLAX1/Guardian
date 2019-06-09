#!/bin/bash

for filename in link_images/*.jpg; do
	#echo $filename
	python detectLocation.py --image=$filename    
done
