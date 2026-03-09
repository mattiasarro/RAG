#!/bin/bash
# /usr/local/bin/openwebui_probe.sh

OPENWEBUI_URL="http://localhost:3000"
API_KEY="your-api-key-here"  # Get from OpenWebUI > Settings > Account > API Keys
LOG_FILE="/var/log/openwebui_probe.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Send a lightweight test query
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$OPENWEBUI_URL/api/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "your-model-name",
    "messages": [{"role": "user", "content": "ping"}],
    "max_tokens": 5
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
  echo "[$TIMESTAMP] OK ($HTTP_CODE)" >> "$LOG_FILE"
else
  echo "[$TIMESTAMP] FAILED ($HTTP_CODE) - $BODY" >> "$LOG_FILE"
  # Optional: restart container on failure
  # docker restart open-webui
  # Optional: send alert
  # curl -s -X POST "https://hooks.slack.com/..." -d '{"text":"OpenWebUI probe failed!"}'
fi
