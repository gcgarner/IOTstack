#!/usr/bin/env bash

# Your DuckDNS domain (or comma-separated list of DuckDNS domains if you
# have multiple domains associated with the same IP address).
DOMAINS="YOURS.duckdns.org"

# Your DuckDNS Token
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"

# is this script running in the foreground or background?
if [ "$(tty)" = "not a tty" ] ; then

   # background! Assume launched by cron. Add a random delay to avoid
   # every client contacting DuckDNS at exactly the same moment.
   sleep $((RANDOM % 60))

fi

# mark the event in case this is being logged.
echo "$(date "+%a, %d %b %Y %H:%M:%S %z") - updating DuckDNS"

# Request duckdns to update your domain name with your public IP address
curl --max-time 10 \
   "https://www.duckdns.org/update?domains=${DOMAINS}&token=${DUCKDNS_TOKEN}&ip="

# curl does not append newline so fix that
echo ""
