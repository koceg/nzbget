#!/bin/bash

NZBADDR=0.0.0.0
NZBUSER=nzbget
NZBPASS=tegbzn6789
NZBSOURCE=/usr/NZB
NZBDESTINATION=/usr
SSHUSER=CHANGE ME
SSHOST=CHANGE ME

rsync -avz --ignore-existing \
      --remove-source-files \
      --exclude='*nzb.queued' \
      $NZBSOURCE $SSHUSER@$SSHOST:$NZBDESTINATION &> /dev/null

sleep 15

./nzbget.py $NZBUSER $NZBPASS $NZBADDR &> /dev/null
