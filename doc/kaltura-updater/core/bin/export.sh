#!/usr/bin/env sh

if [ "$SETUP" != "1" ]; then
	. bin/setup.sh
fi

#init exports caching folder, if missing
if [ ! -d "$EXPORT_PATH" ];
then
	mkdir $EXPORT_PATH
fi

for TAG in $RELEASES
do
	echo "--- Checking $EXPORT_PATH/$TAG"
	if [ ! -d "$EXPORT_PATH/$TAG" ];
	then
		echo "--- No local cache for $TAG found. Starting export"
	  sshpass -p onlyread svn export svn+ssh://svnread@kelev.kaltura.com/usr/local/kalsource/backend/server/tags/$TAG "$EXPORT_PATH/$TAG"
	else 
		echo "--- Local cache found for $TAG. Skipping"
	fi
done
