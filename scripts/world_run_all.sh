#!/bin/bash
# Runs every pass of scripts/world_extract.py in order, retrying the network pass; each pass resumes.
# Waits first for a download that is already running (started separately) to finish.
D=/e/SiteBlitz-World-Business-Data
L=$D/_pipeline.log
cd /e/tmp/Siteblitz_LeadGenerator || exit 1
PY=.venv/Scripts/python.exe
echo "$(date +%H:%M:%S) pipeline started" >> $L
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { \$_.Name -like 'python*' -and \$_.CommandLine -like '*world_extract.py download*' }) { exit 0 } else { exit 1 }"; do
  sleep 30
done
echo "$(date +%H:%M:%S) no other download running" >> $L
for attempt in 1 2 3 4 5; do
  $PY -X utf8 scripts/world_extract.py download >> $L 2>&1
  n=$(ls $D/_work/raw/*.parquet 2>/dev/null | wc -l)
  echo "$(date +%H:%M:%S) download attempt $attempt: $n of 16 files" >> $L
  [ "$n" -ge 16 ] && break
  sleep 60
done
[ "$(ls $D/_work/raw/*.parquet | wc -l)" -ge 16 ] || { echo "PIPELINE FAILED: download incomplete" >> $L; exit 1; }
$PY -X utf8 scripts/world_extract.py split >> $L 2>&1 || { echo "PIPELINE FAILED: split" >> $L; exit 1; }
for attempt in 1 2 3; do
  $PY -X utf8 scripts/world_extract.py export >> $L 2>&1 && break
  echo "$(date +%H:%M:%S) export attempt $attempt failed, resuming" >> $L
done
$PY -X utf8 scripts/world_extract.py summary >> $L 2>&1 || { echo "PIPELINE FAILED: summary" >> $L; exit 1; }
echo "$(date +%H:%M:%S) PIPELINE DONE" >> $L
