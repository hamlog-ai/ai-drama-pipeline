#!/bin/bash
# Reference recipe — copy into the project and edit timings/inputs per cut.
# PER-CUT MIX = dialogue + SFX + (optional) narration. NO music at the cut stage;
# BGM is laid over the concatenated FULL.mp4 at the end (final step below).
# Per cut: native dialogue 1.0 + SFX cues placed on their beats (adelay) +
# optional narration in a silent gap, plus burned-in subtitle PNGs, then concat.
#
# Prereqs:
#   - videos/cutN.mp4         (Seedance renders, 15s, with native dialogue audio)
#   - sfx/<cue>.mp3           (ElevenLabs text_to_sound_effects: poof, cork, whoosh, waves)
#   - subs_png/<id>.png       (from gen_subs.py)
#   - narration/intro.mp3 etc (ElevenLabs, optional)
#
# IMPORTANT: subtitle PNG inputs use `-loop 1 -t 16` so they outlast the cut;
# `-shortest` then trims output to the (shorter) main video length. Each SFX cue
# is positioned in time with `adelay=<ms>|<ms>` on its beat.
set -e
P=subs_png

# overlay chain for 3 timed subtitle PNGs (inputs 1,2,3): aS aE bS bE cS cE
ov() {
  echo "[0:v][1:v]overlay=eof_action=pass:enable='between(t,$1,$2)'[va];[va][2:v]overlay=eof_action=pass:enable='between(t,$3,$4)'[vb];[vb][3:v]overlay=eof_action=pass:enable='between(t,$5,$6)'[v]"
}

# --- CUT 1 (intro narration in the silent opening + an SFX poof on the transform) ---
# inputs: 0 video | 1,2,3 subs | 4 intro VO | 5 SFX poof (fires ~11.0s → adelay 11000)
ffmpeg -y -loglevel error \
  -i videos/cut1.mp4 \
  -loop 1 -t 16 -i $P/c1a.png -loop 1 -t 16 -i $P/c1b.png -loop 1 -t 16 -i $P/c1c.png \
  -i narration/intro.mp3 -i sfx/poof.mp3 \
  -filter_complex "$(ov 0.3 2.8 6.6 9.3 10.5 13.9);[0:a]volume=1.0[a0];[4:a]adelay=300|300,volume=1.4[a1];[5:a]adelay=11000|11000,volume=0.8[a2];[a0][a1][a2]amix=inputs=3:duration=first:normalize=0[aout]" \
  -map "[v]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest videos/cut1_final.mp4

# --- CUTS 2..N (dialogue + SFX cues; narration only if a real gap exists) ---
# inputs: 0 video | 1,2,3 subs | 4 SFX cue (e.g. cork pop / throw whoosh on its beat)
ffmpeg -y -loglevel error \
  -i videos/cut2.mp4 \
  -loop 1 -t 16 -i $P/c2a.png -loop 1 -t 16 -i $P/c2b.png -loop 1 -t 16 -i $P/c2c.png \
  -i sfx/whoosh.mp3 \
  -filter_complex "$(ov 0.5 2.8 5.2 9.0 10.0 14.0);[0:a]volume=1.0[a0];[4:a]adelay=11000|11000,volume=0.8[a1];[a0][a1]amix=inputs=2:duration=first:normalize=0[aout]" \
  -map "[v]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest videos/cut2_final.mp4

# (repeat for cut3 / cut4, adjusting subtitle timings and SFX beats)

# --- concat -> FULL.mp4 (SFX-only intermediate; kept as a fallback) ---
printf "file 'cut1_final.mp4'\nfile 'cut2_final.mp4'\nfile 'cut3_final.mp4'\nfile 'cut4_final.mp4'\n" > videos/concat_list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i videos/concat_list.txt \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k videos/FULL.mp4
echo "done -> videos/FULL.mp4"

# --- Background-music pass (DEFAULT final step; see workflow §9) ---
# One continuous Suno instrumental (music/bgm.mp3) matched to the full runtime,
# mixed UNDER dialogue+SFX at ~0.10. FULL_bgm.mp4 is the headline deliverable;
# the SFX-only FULL.mp4 stays intact as a fallback.
# Length mismatch handling:
#   - track SHORTER than video: `-stream_loop -1` loops it; amix duration=first
#     trims to the video (without the loop the music just stops mid-video)
#   - track LONGER: trimmed automatically by duration=first
#   - either way `afade=t=out` gives a 2s fade so the music never cuts abruptly
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 videos/FULL.mp4)
FADE_ST=$(python3 -c "print(max(0, $DUR - 2))")
ffmpeg -y -loglevel error -i videos/FULL.mp4 -stream_loop -1 -i music/bgm.mp3 -filter_complex \
  "[1:a]volume=0.10,afade=t=out:st=$FADE_ST:d=2[bg];[0:a][bg]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k videos/FULL_bgm.mp4
echo "done -> videos/FULL_bgm.mp4"

# Optional platform-loudness pass (shorts/reels target ≈ -14 LUFS) — re-encodes
# audio only; run if the mix sounds quiet/hot on the target platform:
#   ffmpeg -y -i videos/FULL_bgm.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 \
#     -c:v copy -c:a aac -b:a 192k videos/FULL_bgm_norm.mp4

# Timing: take subtitle windows and narration gaps from the QC-gate STT
# transcripts (qc/cutN_stt.json — word timestamps ±0.2s), per workflow §8.
# Fallback if STT failed on a cut — locate speech/gaps with:
#   ffmpeg -i videos/cutN.mp4 -af silencedetect=noise=-30dB:d=0.4 -f null -
# Vertical (9:16) projects: subtitle PNGs come from gen_subs.py with
#   --w 720 --h 1280 --margin 190  (see workflow §1/§8).
