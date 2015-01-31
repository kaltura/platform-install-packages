#!/bin/sh
file=debian/br.$1
current=`cat $file 2>/dev/null`
if [ "$2" = "inc" ]; then
	next=`expr $current + 1`
	echo $next > $file 
	# if this is binary-indep, we want both br files to be promoted
	if grep -q "binary: binary-indep" debian/rules;then
		if [ $1 = 'i386' ];then
			cp $file debian/br.amd64
		else
			cp $file debian/br.i386
		fi
	fi
	# we want to be able to remove it when committing a new version to the changelog file so that the counter is reset.
	chmod 666 $file
fi
echo $current
