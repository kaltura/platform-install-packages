#!/usr/bin/env sh

#for FILE in $(find . -type f -name *.sql); do sed -i "s^p_20141025^@PARTITION_NAME@^" $FILE; done

echo "Building DWH sources"

SOURCE_DIR="sources"
BUILD_DIR="build"

if [ ! -d $SOURCE_DIR ];
then
  echo "ERROR: sources folder missing. Exiting."
  exit 1
fi

if [ -d $BUILD_DIR ];
then
  rm -Rf $BUILD_DIR;
fi

cp -R $SOURCE_DIR $BUILD_DIR

PARTITION_VALUE=$(date +%Y%m%d)
PARTITION_NAME=$(date -d "-1 day" +%Y%m%d)

echo "Replacing partition token values p_$PARTITION_NAME = $PARTITION_VALUE"

for FILE in $(find $BUILD_DIR -type f -name *.sql);
do

 sed -i "s^@PARTITION_NAME@^p_$PARTITION_NAME^" $FILE
 sed -i "s^@PARTITION_VALUE@^$PARTITION_VALUE^" $FILE

done
