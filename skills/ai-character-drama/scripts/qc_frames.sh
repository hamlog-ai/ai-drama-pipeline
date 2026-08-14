#!/bin/bash
# Extract evenly-spaced QC frames from rendered cuts for the visual QC gate
# (workflow §6b): Read the frames next to the registered character sheets /
# prop shots to confirm faces, props, environment, style, and aspect ratio.
#
# Usage:
#   bash qc_frames.sh videos/cut1.mp4 [videos/cut2.mp4 ...]
#   QC_FRAMES=8 bash qc_frames.sh videos/cut1.mp4    # more frames per cut
#
# Output: qc/<cutname>/f01.jpg ... (default 6 frames, 800px wide)
set -e
N=${QC_FRAMES:-6}
for v in "$@"; do
  name=$(basename "${v%.*}")
  out="qc/$name"
  mkdir -p "$out"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
  ffmpeg -y -loglevel error -i "$v" \
    -vf "fps=$N/$dur,scale=800:-2" -frames:v "$N" "$out/f%02d.jpg"
  echo "-> $out ($N frames over ${dur%s}s)"
done
