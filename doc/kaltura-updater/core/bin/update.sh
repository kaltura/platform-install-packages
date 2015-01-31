#!/usr/bin/env sh

echo "-- Starting udpate process"
echo "-- Parse & prompt update"
. bin/setup.sh

echo "-- Checkout all releases to exports"
. bin/export.sh

echo "-- Creating instance configurations"
. bin/configure.sh

echo "-- Creating instance configurations"
. bin/run-update.sh