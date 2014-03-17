#!/bin/bash - 
#===============================================================================
#
#          FILE:  colors.sh
# 
#         USAGE:  ./colors.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#       COMPANY: 
#       CREATED: 07/27/2011 11:42:19 AM IDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

DULL=0
BRIGHT=1

FG_BLACK=30
FG_RED=31
FG_GREEN=32
FG_YELLOW=33
FG_BLUE=34
FG_VIOLET=35
FG_CYAN=36
FG_WHITE=37

FG_NULL=00

BG_BLACK=40
BG_RED=41
BG_GREEN=42
BG_YELLOW=43
BG_BLUE=44
BG_VIOLET=45
BG_CYAN=46
BG_WHITE=47

BG_NULL=00
ETCOLOR_ERROR="\\033[1;31m"
##
# ANSI Escape Commands
##
ESC="\033"
NORMAL="\033[m"
RESET="\\${ESC}[${DULL};${FG_WHITE};${BG_NULL}m"

##
# Shortcuts for Colored Text ( Bright and FG Only )
##

# DULL TEXT
BLACK="\033[${DULL};${FG_BLACK}m"
RED="\033[${DULL};${FG_RED}m"
GREEN="\033[${DULL};${FG_GREEN}m"
YELLOW="\033[${DULL};${FG_YELLOW}m"
BLUE="\033[${DULL};${FG_BLUE}m"
VIOLET="\033[${DULL};${FG_VIOLET}m"
CYAN="\033[${DULL};${FG_CYAN}m"
WHITE="\033[${DULL};${FG_WHITE}m"

# BRIGHT TEXT
BRIGHT_BLACK="\033[${BRIGHT};${FG_BLACK}m"
BRIGHT_RED="\033[${BRIGHT};${FG_RED}m"
BRIGHT_GREEN="\033[${BRIGHT};${FG_GREEN}m"
BRIGHT_YELLOW="\033[${BRIGHT};${FG_YELLOW}m"
BRIGHT_BLUE="\033[${BRIGHT};${FG_BLUE}m"
BRIGHT_VIOLET="\\${ESC}[${BRIGHT};${FG_VIOLET}m"
BRIGHT_CYAN="\033[${BRIGHT};${FG_CYAN}m"
BRIGHT_WHITE="\033[${BRIGHT};${FG_WHITE}m"

# REV TEXT as an example
REV_CYAN="\033[${DULL};${BG_WHITE};${BG_CYAN}m"
REV_RED="\033[${DULL};${FG_YELLOW}; ${BG_RED}m"

JESS="Jess likes this one :)"
#echo -e "${BRIGHT_BLUE}What's up?${NORMAL}"
#echo -e "${BRIGHT_BLUE}$JESS${NORMAL}"
#echo -e "${YELLOW}Jess likes this one :)${NORMAL}"

