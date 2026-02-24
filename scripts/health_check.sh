#!/bin/bash
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:8080/health --connect-timeout 5 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo "HEALTHY"
    exit 0
else
    echo "UNHEALTHY (HTTP $RESPONSE)"
    exit 1
fi
