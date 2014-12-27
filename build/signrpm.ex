#!/usr/bin/expect -f
#
# rpmsign-batch.expect : expect powered rpm signing command
#

proc usage {} {
        send_user "Usage: signrpm.ex /path/to/rpmfile\n\n"
        exit
}

if {[llength $argv]!=1} usage

set rpmfile [lrange $argv 0 0]


spawn rpm --addsign  $rpmfile
expect -exact "Enter pass phrase: "
send -- "\r"
expect eof

