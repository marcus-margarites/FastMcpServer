rem @echo off
rem call init.cmd
curl -sS -X POST http://localhost:8000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: ebe6a324fbb94f8f8d999dd6e28cb060" -d @list_tools.json
