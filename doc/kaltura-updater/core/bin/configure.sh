#!/usr/bin/env sh

if [ "$SETUP" != "1" ]; then
	. bin/setup.sh
fi

for RELEASE in $RELEASES; do
 echo "--- Creating configuration for $RELEASE"

 cp asset/db.template.ini "$EXPORT_PATH/$RELEASE/configurations/db.ini"
 cp asset/local.template.ini "$EXPORT_PATH/$RELEASE/configurations/local.ini"
 cp asset/dc_config.template.ini "$EXPORT_PATH/$RELEASE/configurations/dc_config.ini"
 cp asset/logger.template.ini "$EXPORT_PATH/$RELEASE/configurations/logger.ini"

 sed -i "s^@ROOT_USER@^$MYSQL_ROOT^" "$EXPORT_PATH/$RELEASE/configurations/db.ini"
 sed -i "s^@ROOT_PASSWORD@^$MYSQL_ROOT_PW^" "$EXPORT_PATH/$RELEASE/configurations/db.ini"


 sed -i "s^@ROOT_USER@^$MYSQL_ROOT^" "$EXPORT_PATH/$RELEASE/configurations/local.ini"
 sed -i "s^@ROOT_PASSWORD@^$MYSQL_ROOT_PW^" "$EXPORT_PATH/$RELEASE/configurations/local.ini"
 sed -i "s^@INSTANCE_PATH@^$EXPORT_PATH/$RELEASE^" "$EXPORT_PATH/$RELEASE/configurations/local.ini"

 sed -i "s^@SERVICE_URL@^$SERVICE_URL^" "$EXPORT_PATH/$RELEASE/configurations/dc_config.ini"
 sed -i "s^@WEB_DIR@^$WEB_DIR^" "$EXPORT_PATH/$RELEASE/configurations/dc_config.ini"

  

 sed -i "s^@LOG_DIR@^$LOG_FOLDER^" "$EXPORT_PATH/$RELEASE/configurations/logger.ini"

 # for FILE in $(find $EXPORT_PATH/$RELEASE/deployment -type f -name '*.php'); do sed -i "s^usleep^#usleep^" $FILE; done
 # for FILE in $(find $EXPORT_PATH/$RELEASE/deployment -type f -name '*.php'); do sed -i "s^sleep^#sleep^" $FILE; done

done;
