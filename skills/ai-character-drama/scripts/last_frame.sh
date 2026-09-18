#!/bin/bash
# Extract the LAST frame of a rendered cut as the continuity anchor for the next
# cut (workflow §6a — Anchor-and-Extend). The frame is uploaded to the video
# provider and passed as `start_image` (or registered as a continuity Element)
# so CUT N+1 opens exactly where CUT N ended: same place, same camera height,
# same blocking, same prop state.
#
# Usage:
#   bash last_frame.sh videos/cut1.mp4              # → continuity/cut1_last.jpg
#   bash last_frame.sh videos/cut1.mp4 videos/cut2.mp4
#   LAST_OFFSET=0.5 bash last_frame.sh videos/cut1.mp4   # step 0.5s back from the
#       end if the true final frame is a fade/black/motion-blurred frame
#   OUT_DIR=qc bash last_frame.sh videos/cut1.mp4   # different output folder
#
# Output: <OUT_DIR>/<cutname>_last.jpg (full resolution, high quality).
# Always Read the jpg before using it — a black, blurred or mid-cut-transition
# frame anchors the next cut to garbage. If it's bad, re-run with LAST_OFFSET.
set -e
OFF=${LAST_OFFSET:-0}
OUT_DIR=${OUT_DIR:-continuity}
mkdir -p "$OUT_DIR"
for v in "$@"; do
  name=$(basename "${v%.*}")
  out="$OUT_DIR/${name}_last.jpg"
  if [ "$OFF" = "0" ]; then
    # Seek to the last ~0.5s and keep overwriting the single output until the
    # stream ends → the file holds the true final decoded frame.
    ffmpeg -y -loglevel error -sseof -0.5 -i "$v" -update 1 -q:v 1 "$out"
  else
    ffmpeg -y -loglevel error -sseof "-$OFF" -i "$v" -frames:v 1 -q:v 1 "$out"
  fi
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
  echo "-> $out (from ${dur%s}s cut, offset ${OFF}s before end)"
done
