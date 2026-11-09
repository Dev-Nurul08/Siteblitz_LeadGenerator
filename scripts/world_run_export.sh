#!/bin/bash
# Export every country again in the v2 layout (ISO state names), then the world summary.
# Each country is resumable (.done with "v2"); retried up to 3 times.
D=/e/SiteBlitz-World-Business-Data
L=$D/_pipeline.log
cd /e/tmp/Siteblitz_LeadGenerator || exit 1
PY=.venv/Scripts/python.exe
echo "$(date +%H:%M:%S) export v2 started (ISO state names)" >> $L
for attempt in 1 2 3; do
  $PY -X utf8 scripts/world_extract.py export --redo >> $L 2>&1 && break
  echo "$(date +%H:%M:%S) export attempt $attempt failed, resuming" >> $L
done
$PY -X utf8 scripts/world_extract.py summary >> $L 2>&1 || { echo "PIPELINE FAILED: summary" >> $L; exit 1; }
echo "$(date +%H:%M:%S) PIPELINE DONE" >> $L
