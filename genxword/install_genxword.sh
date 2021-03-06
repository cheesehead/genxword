#!/bin/sh
# Script to install genxword, which depends on python 2.7 and py2cairo.
# genxword-gtk also depends on python-gobject and gtksourceview3

ERROR_MESSAGE="$(tput bold)$(tput setaf 1)An error occurred. \
Please read the output above to see what the problem is.$(tput sgr0)\n"
MAN_DIR=/usr/share/man/man1

python2.7 setup.py install --optimize=1 || { printf "$ERROR_MESSAGE"; exit 1; }
APP_NAME=genxword

printf "Installing the man pages for $APP_NAME and $APP_NAME-gtk\n"
cp $APP_NAME.1 $MAN_DIR && gzip -f $MAN_DIR/$APP_NAME.1 || printf "The man page could not be installed\n"
cp $APP_NAME-gtk.1 $MAN_DIR && gzip -f $MAN_DIR/$APP_NAME-gtk.1 || printf "The man page could not be installed\n"

printf "$(tput setaf 2)The programs $APP_NAME and $APP_NAME-gtk have been installed.$(tput sgr0)\n"
