#!/usr/bin/env sh

if [ "$SETUP" != "1" ]; then
	. bin/setup.sh
fi

for RELEASE in $RELEASES; do
 echo "--- Running update.php for $RELEASE"
 cd "$EXPORT_PATH/$RELEASE/deployment/updates"
 php "update.php" >> "$LOG_FOLDER/update.log" 2> "$LOG_FOLDER/update.error.log"
done;
