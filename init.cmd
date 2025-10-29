rem @echo off
curl -i -sS -X POST http://localhost:8000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d @init.json
