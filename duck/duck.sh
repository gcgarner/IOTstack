#!/bin/bash
# Your comma-separated domains list
DOMAINS="YOUR_DOMAINS"
# Your DuckDNS Token
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"

# A random delay to avoid every client contacting the duckdns server at the same moment
sleep $((RANDOM % 60))
# Request duckdns to update your domain name with your public IP address
curl --silent --max-time 10 --output /dev/null "https://www.duckdns.org/update?domains=${DOMAINS}&token=${DUCKDNS_TOKEN}&ip="
