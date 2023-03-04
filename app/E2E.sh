#!/bin/bash
set -e

# Get list of series from main page
series=$(curl -s localhost | grep -oP '(?<=href="/file_list/)[^"]*')

# Loop through series and create directory for each
for s in $series
do
  mkdir -p "$s"

  # Curl the file list for each series and get list of episodes
  episodes=$(curl -s localhost/file_list/$s | grep -oP '(?<=data-episode=")[^"]*')

  # Loop through episodes and download each file
  for e in $episodes
  do
    curl -o "$s/$s-Episode-$e.mp4" "localhost/play/$s-S01E$e.mp4"
  done
done
