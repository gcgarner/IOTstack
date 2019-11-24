#!/bin/bash
# Your comma-separated domains list
DOMAINS="YOUR_DOMAINS"
# Your DuckDNS Token
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"
curl -k -o /var/log/duck.log "https://www.duckdns.org/update?domains=${DOMAINS}&token=${DUCKDNS_TOKEN}&ip="
