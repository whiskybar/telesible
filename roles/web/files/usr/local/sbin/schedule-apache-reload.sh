#!/bin/bash

MINUTES=5
SECONDS=$(( $MINUTES * 60 ))
NEXT_RUN=$(( $(date +%s) / $SECONDS * $SECONDS + $SECONDS))

# check if the reload has been scheduled
atq | cut -c3-26 | xargs -I DATE date -d"DATE" +%s | grep -q $NEXT_RUN && exit 0

echo 'systemctl reload apache2' | at $(date -d@$NEXT_RUN +%H:%M) >/dev/null


